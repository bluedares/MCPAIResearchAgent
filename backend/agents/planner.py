"""Planner agent - generates research plan with sub-queries."""
import os
import sys
from typing import Dict, Any
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langsmith import traceable

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings


class ResearchPlan(BaseModel):
    """Structured research plan output."""
    
    main_topic: str = Field(description="The main research topic")
    sub_queries: list[str] = Field(
        description="3-5 specific sub-queries to investigate",
        min_items=3,
        max_items=5
    )
    research_approach: str = Field(description="Brief description of research approach")


@traceable(name="planner_agent", run_type="llm")
async def plan_research(topic: str) -> Dict[str, Any]:
    """
    Generate a research plan with sub-queries.
    
    Args:
        topic: Research topic from user
        
    Returns:
        Dictionary with research plan and sub-queries
    """
    # Initialize Claude
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0.3,
        api_key=settings.anthropic_api_key
    )
    
    # Create structured output LLM
    structured_llm = llm.with_structured_output(ResearchPlan)
    
    # Create prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a research planning expert. Given a topic, create a comprehensive research plan.

Your task:
1. Break down the topic into 3-5 specific, focused sub-queries
2. Each sub-query should investigate a different aspect of the topic
3. Sub-queries should be specific enough to get concrete search results
4. Describe your overall research approach

Be thorough but focused. Prioritize recent, factual information."""),
        ("human", "Research topic: {topic}")
    ])
    
    # Generate plan
    chain = prompt | structured_llm
    plan = await chain.ainvoke({"topic": topic})
    
    return {
        "main_topic": plan.main_topic,
        "sub_queries": plan.sub_queries,
        "research_approach": plan.research_approach
    }
