"""LangGraph workflow orchestration for research agent."""
import uuid
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.aiosqlite import AsyncSqliteSaver
from langsmith import traceable
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.state import ResearchState
from agents.planner import plan_research
from agents.retriever import retrieve_information
from agents.summarizer import summarize_research
from agents.verifier import verify_research
from agents.email_sender import send_research_email


# Node functions
async def planner_node(state: ResearchState) -> Dict[str, Any]:
    """Planner node - generates research plan."""
    state["status_messages"].append("🧠 Planning research strategy...")
    
    plan = await plan_research(state["topic"])
    
    return {
        "research_plan": plan,
        "sub_queries": plan["sub_queries"],
        "current_step": "retriever",
        "status_messages": state["status_messages"] + [
            f"✅ Generated {len(plan['sub_queries'])} sub-queries"
        ]
    }


async def retriever_node(state: ResearchState) -> Dict[str, Any]:
    """Retriever node - searches web for information."""
    state["status_messages"].append("🔍 Searching web for information...")
    
    results = await retrieve_information(state["sub_queries"])
    
    return {
        "raw_data": results["raw_data"],
        "sources": results["sources"],
        "current_step": "summarizer",
        "status_messages": state["status_messages"] + [
            f"✅ Retrieved {len(results['raw_data'])} results from {len(results['sources'])} sources"
        ]
    }


async def summarizer_node(state: ResearchState) -> Dict[str, Any]:
    """Summarizer node - synthesizes findings."""
    state["status_messages"].append("📝 Synthesizing research findings...")
    
    summary_result = await summarize_research(
        state["topic"],
        state["raw_data"],
        state["sources"]
    )
    
    return {
        "summary": summary_result["summary"],
        "citations": summary_result["citations"],
        "current_step": "verifier",
        "status_messages": state["status_messages"] + [
            f"✅ Created summary with {len(summary_result['citations'])} citations"
        ]
    }


async def verifier_node(state: ResearchState) -> Dict[str, Any]:
    """Verifier node - validates summary."""
    state["status_messages"].append("✅ Verifying accuracy and citations...")
    
    verification = await verify_research(
        state,  # Pass state as first argument
        state["summary"],
        state["citations"],
        state["sources"]
    )
    
    # Return all verification fields including verified flag
    return verification


async def email_sender_node(state: ResearchState) -> Dict[str, Any]:
    """Email sender node - sends research via Gmail."""
    import logging
    logger = logging.getLogger(__name__)
    
    state["status_messages"].append(f" Sending email to {state['client_email']}...")
    
    logger.info(f"📧 Email sender received: summary_len={len(state.get('summary', ''))}, citations={len(state.get('citations', []))}")
    
    email_result = await send_research_email(
        state["topic"],
        state["client_email"],
        state["summary"],
        state.get("research_plan", {}).get("key_findings", []),
        state["citations"]
    )
    
    # CRITICAL: Must preserve summary and citations in return
    return {
        "summary": state["summary"],  # Preserve summary
        "citations": state["citations"],  # Preserve citations
        "verified": state.get("verified", True),  # Preserve verification status
        "verification_status": state.get("verification_status", ""),
        "verification_confidence": state.get("verification_confidence", 0),
        "email_sent": email_result["email_sent"],
        "email_timestamp": email_result.get("email_timestamp"),
        "final_output": state["summary"],
        "current_step": "complete",
        "status_messages": state["status_messages"] + [
            " Email sent successfully!" if email_result["email_sent"] else " Email failed to send"
        ]
    }


# Conditional edge function
def should_retry_summary(state: ResearchState) -> str:
    """Determine if summary needs revision."""
    import logging
    logger = logging.getLogger(__name__)
    
    retry_count = state.get("retry_count", 0)
    verification_status = state.get("verification_status", "unknown")
    
    logger.info(f"🔀 Routing decision: status={verification_status}, retry_count={retry_count}")
    
    # If verification failed and retry_count is 0, retry once
    if verification_status == "fail" and retry_count < 1:
        logger.info("🔄 Retrying summarization (attempt 1)")
        return "summarizer"
    
    # Otherwise always proceed to email (either passed or max retries reached)
    logger.info("➡️ Proceeding to email sender")
    return "email_sender"


# Build workflow
def create_workflow() -> StateGraph:
    """Create the research workflow graph."""
    
    # Initialize graph
    workflow = StateGraph(ResearchState)
    
    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("retriever", retriever_node)
    workflow.add_node("summarizer", summarizer_node)
    workflow.add_node("verifier", verifier_node)
    workflow.add_node("email_sender", email_sender_node)
    
    # Add edges
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "retriever")
    workflow.add_edge("retriever", "summarizer")
    workflow.add_edge("summarizer", "verifier")
    
    # Conditional edge from verifier
    workflow.add_conditional_edges(
        "verifier",
        should_retry_summary,
        {
            "summarizer": "summarizer",
            "email_sender": "email_sender"
        }
    )
    
    workflow.add_edge("email_sender", END)
    
    return workflow


# Compile workflow with checkpointing
async def get_compiled_workflow():
    """Get compiled workflow with async SQLite checkpointing."""
    workflow = create_workflow()
    
    # Create async checkpointer
    os.makedirs("./data", exist_ok=True)
    checkpointer = AsyncSqliteSaver.from_conn_string("./data/checkpoints.db")
    
    # Compile
    app = workflow.compile(checkpointer=checkpointer)
    
    return app


# Execute workflow
@traceable(name="research_workflow", run_type="chain")
async def run_research_workflow(topic: str, client_email: str) -> Dict[str, Any]:
    """
    Execute the complete research workflow.
    
    Args:
        topic: Research topic
        client_email: Client email address
        
    Returns:
        Final state with results
    """
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
        "verification_feedback": None,
        "final_output": "",
        "email_sent": False,
        "email_timestamp": None,
        "workflow_id": str(uuid.uuid4()),
        "current_step": "planner",
        "errors": [],
        "retry_count": 0,
        "status_messages": []
    }
    
    # Run workflow
    config = {"configurable": {"thread_id": initial_state["workflow_id"]}}
    
    final_state = None
    async for state in app.astream(initial_state, config):
        final_state = state
    
    return final_state
