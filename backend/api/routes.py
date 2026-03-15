"""API routes for research workflow."""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, EmailStr, Field
from typing import AsyncGenerator
import json
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.workflow import get_compiled_workflow
from graph.state import ResearchState
from config.settings import settings
from agents.email_sender import send_research_email

router = APIRouter()


class ResearchRequest(BaseModel):
    """Research request model."""
    topic: str = Field(..., min_length=10, max_length=500, description="Research topic")
    client_email: EmailStr = Field(..., description="Client email address")


class ResearchResponse(BaseModel):
    """Research response model."""
    workflow_id: str
    status: str
    message: str


class ConfigResponse(BaseModel):
    """Configuration response model."""
    email_enabled: bool


class SendEmailRequest(BaseModel):
    """Send email request model."""
    email: EmailStr = Field(..., description="Recipient email address")
    topic: str = Field(..., description="Research topic")
    summary: str = Field(..., description="Research summary")
    citations: list = Field(default=[], description="Citations")


@router.post("/research", response_model=ResearchResponse)
async def start_research(request: ResearchRequest):
    """
    Start a research workflow.
    
    Args:
        request: Research request with topic and email
        
    Returns:
        Workflow ID and status
    """
    import uuid
    
    workflow_id = str(uuid.uuid4())
    
    return ResearchResponse(
        workflow_id=workflow_id,
        status="started",
        message=f"Research workflow started for topic: {request.topic}"
    )


@router.get("/research/{workflow_id}/stream")
async def stream_research_status(workflow_id: str, topic: str, client_email: str):
    """
    Stream research workflow status updates via Server-Sent Events.
    
    Args:
        workflow_id: Workflow ID
        topic: Research topic
        client_email: Client email
        
    Returns:
        SSE stream of status updates
    """
    
    async def event_generator() -> AsyncGenerator[str, None]:
        """Generate SSE events for workflow progress."""
        try:
            from utils.redis_cache import get_cached_research, cache_research
            from agents.topic_validator import validate_topic
            
            # Validate topic first
            validation = await validate_topic(topic)
            if not validation["is_valid"]:
                # Send validation error
                error_event = {
                    "type": "validation_error",
                    "error": validation["reason"],
                    "suggestion": validation["suggestion"]
                }
                yield f"data: {json.dumps(error_event)}\n\n"
                return
            
            # Check cache first
            cached_result = await get_cached_research(topic, client_email)
            if cached_result:
                # Send start event
                yield f"data: {json.dumps({'type': 'start', 'workflow_id': workflow_id, 'from_cache': True})}\n\n"
                
                # Send cached completion immediately
                final_event = {
                    "type": "complete",
                    "email_sent": False,
                    "summary": cached_result.get("summary", ""),
                    "citations": cached_result.get("citations", []),
                    "verified": cached_result.get("verified", True),
                    "verification_status": "pass",
                    "verification_confidence": 1.0,
                    "from_cache": True
                }
                yield f"data: {json.dumps(final_event)}\n\n"
                return
            
            app = await get_compiled_workflow()
            
            # Initialize state
            initial_state: ResearchState = {
                "topic": topic,
                "client_email": client_email,
                "research_plan": None,
                "sub_queries": [],
                "raw_data": [],
                "sources": [],
                "summary": "",
                "citations": [],
                "verification_status": "",
                "verification_confidence": 0.0,
                "verification_feedback": "",
                "verified": True,
                "final_output": "",
                "email_sent": False,
                "email_timestamp": None,
                "workflow_id": workflow_id,
                "current_step": "planner",
                "errors": [],
                "retry_count": 0,
                "status_messages": []
            }
            
            # Send start event
            yield f"data: {json.dumps({'type': 'start', 'workflow_id': workflow_id})}\n\n"
            
            # Run workflow and stream updates
            config = {"configurable": {"thread_id": workflow_id}}
            
            final_state = {}  # Initialize final state
            
            async for state in app.astream(initial_state, config):
                # Extract current state
                current_state = list(state.values())[0] if state else {}
                final_state = current_state  # Keep updating final state
                
                # Send status update
                event_data = {
                    "type": "update",
                    "step": current_state.get("current_step", "unknown"),
                    "messages": current_state.get("status_messages", []),
                    "verification_status": current_state.get("verification_status", ""),
                }
                
                yield f"data: {json.dumps(event_data)}\n\n"
                
                # Small delay for readability
                await asyncio.sleep(0.1)
            
            # Send completion event with all necessary data from final state
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"📤 Sending completion event: summary_len={len(final_state.get('summary', ''))}, citations={len(final_state.get('citations', []))}")
            
            final_event = {
                "type": "complete",
                "email_sent": final_state.get("email_sent", False),
                "summary": final_state.get("summary", ""),
                "citations": final_state.get("citations", []),
                "verified": final_state.get("verified", True),
                "verification_status": final_state.get("verification_status", ""),
                "verification_confidence": final_state.get("verification_confidence", 0),
                "from_cache": False
            }
            
            # Cache the results for future use (fire and forget)
            if final_state.get("summary"):
                await cache_research(
                    topic=topic,
                    client_email=client_email,
                    summary=final_state.get("summary", ""),
                    citations=final_state.get("citations", []),
                    verified=final_state.get("verified", True),
                    ttl_hours=24  # Cache for 24 hours
                )
            
            yield f"data: {json.dumps(final_event)}\n\n"
            
        except Exception as e:
            # Send error event
            error_event = {
                "type": "error",
                "error": str(e)
            }
            yield f"data: {json.dumps(error_event)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.get("/config", response_model=ConfigResponse)
async def get_config():
    """
    Get application configuration.
    
    Returns:
        Configuration including feature flags
    """
    return ConfigResponse(email_enabled=settings.email_enabled)


@router.post("/send-email")
async def send_email_endpoint(request: SendEmailRequest):
    """
    Send research results via email after research completion.
    
    Args:
        request: Email request with recipient, topic, summary, and citations
        
    Returns:
        Email send status
    """
    if not settings.email_enabled:
        raise HTTPException(status_code=403, detail="Email functionality is disabled")
    
    try:
        result = await send_research_email(
            topic=request.topic,
            client_email=request.email,
            summary=request.summary,
            key_findings=[],
            citations=request.citations
        )
        
        return {
            "success": result["email_sent"],
            "message": "Email sent successfully" if result["email_sent"] else "Failed to send email",
            "timestamp": result.get("email_timestamp")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


@router.post("/research/execute")
async def execute_research(request: ResearchRequest):
    """
    Execute research workflow synchronously (for testing).
    
    Args:
        request: Research request
        
    Returns:
        Complete research results
    """
    try:
        from graph.workflow import run_research_workflow
        
        result = await run_research_workflow(request.topic, request.client_email)
        
        # Extract final state
        final_state = list(result.values())[0] if result else {}
        
        return {
            "workflow_id": final_state.get("workflow_id", "unknown"),
            "status": "completed" if final_state.get("email_sent") else "failed",
            "summary": final_state.get("summary", ""),
            "citations": final_state.get("citations", []),
            "email_sent": final_state.get("email_sent", False),
            "status_messages": final_state.get("status_messages", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
