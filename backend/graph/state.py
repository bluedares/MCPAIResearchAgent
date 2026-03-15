"""LangGraph state schema for research workflow."""
from typing import TypedDict, List, Dict, Optional, Any


class ResearchState(TypedDict):
    """State for the research workflow."""
    
    # User inputs
    topic: str
    client_email: str
    
    # Planner outputs
    research_plan: Optional[Dict[str, Any]]
    sub_queries: List[str]
    
    # Retriever outputs
    raw_data: List[Dict[str, Any]]
    sources: List[str]
    
    # Summarizer outputs
    summary: str
    citations: List[Dict[str, str]]
    
    # Verification
    verification_status: str
    verification_confidence: float
    verification_feedback: str
    verified: bool = True  # True if verified, False if "Not Verified"
    
    # Final outputs
    final_output: str
    email_sent: bool
    email_timestamp: Optional[str]
    
    # Metadata
    workflow_id: str
    current_step: str
    errors: List[str]
    retry_count: int
    
    # Status messages for streaming
    status_messages: List[str]
