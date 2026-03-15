"""Summarizer agent - synthesizes research findings with citations."""
import os
import sys
from typing import List, Dict, Any
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langsmith import traceable

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings


class Citation(BaseModel):
    """Citation model."""
    claim: str = Field(description="The claim being cited")
    source_url: str = Field(description="URL of the source")
    source_title: str = Field(description="Title of the source")


class ResearchSummary(BaseModel):
    """Structured research summary with citations."""
    
    summary: str = Field(description="Comprehensive research summary (500-1000 words)")
    key_findings: list[str] = Field(default=[], description="3-5 key findings from the research")
    citations: list[Citation] = Field(default=[], description="Citations for claims made")


@traceable(name="summarizer_agent", run_type="llm")
async def summarize_research(
    topic: str,
    raw_data: List[Dict[str, Any]],
    sources: List[str]
) -> Dict[str, Any]:
    """
    Synthesize research findings into a comprehensive summary.
    
    Args:
        topic: Original research topic
        raw_data: Raw search results
        sources: List of source URLs
        
    Returns:
        Dictionary with summary and citations
    """
    # Initialize Claude
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0.2,
        api_key=settings.anthropic_api_key
    )
    
    # Create structured output LLM
    structured_llm = llm.with_structured_output(ResearchSummary)
    
    # Format research data for prompt
    formatted_data = []
    for i, item in enumerate(raw_data[:20], 1):  # Limit to top 20 results
        formatted_data.append(f"""
Source {i}:
Query: {item.get('query', 'N/A')}
Title: {item.get('title', 'N/A')}
URL: {item.get('url', 'N/A')}
Content: {item.get('content', 'N/A')}
""")
    
    research_context = "\n".join(formatted_data)
    
    # Create prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a research synthesis expert. Create a comprehensive research summary.

Your task:
1. Write a clear, informative **summary** (300-800 words) that:
   - Introduces the topic
   - Presents main findings organized by theme
   - Concludes with key takeaways
   - Mentions sources inline (e.g., "According to [source title]...")

2. List 3-5 **key_findings** as bullet points

3. Create **citations** for major claims:
   - claim: The specific statement being cited
   - source_url: URL from the provided sources
   - source_title: Title of the source

Guidelines:
- Be objective and balanced
- Use clear, professional language
- Focus on the most important information
- If sources are limited, work with what's available
- It's better to have a good summary with few citations than no summary at all"""),
        ("human", """Research Topic: {topic}

Research Data:
{research_context}

Available Sources:
{sources}

Create a comprehensive research summary with proper citations.""")
    ])
    
    # Generate summary with error handling
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        chain = prompt | structured_llm
        result = await chain.ainvoke({
            "topic": topic,
            "research_context": research_context,
            "sources": "\n".join(f"- {url}" for url in sources)
        })
        
        # Validate result
        if not result or not hasattr(result, 'summary') or not result.summary:
            logger.warning("⚠️ Claude returned empty structured output, using fallback")
            raise ValueError("Empty structured output from Claude")
        
        logger.info(f"✅ Generated summary: {len(result.summary)} chars, {len(result.citations)} citations")
        
        return {
            "summary": result.summary,
            "key_findings": result.key_findings if result.key_findings else [],
            "citations": [
                {
                    "claim": cite.claim,
                    "source_url": cite.source_url,
                    "source_title": cite.source_title
                }
                for cite in (result.citations if result.citations else [])
            ]
        }
    except Exception as e:
        logger.error(f"❌ Structured output failed: {e}, using fallback text generation")
        
        # Fallback: Use regular LLM without structured output
        llm_fallback = ChatAnthropic(
            model="claude-sonnet-4-20250514",
            temperature=0.2,
            api_key=settings.anthropic_api_key
        )
        
        fallback_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a research synthesis expert. Create a comprehensive research summary (300-800 words) based on the provided sources. Be objective and informative."),
            ("human", """Research Topic: {topic}

Research Data:
{research_context}

Write a comprehensive summary of the research findings.""")
        ])
        
        fallback_chain = fallback_prompt | llm_fallback
        fallback_result = await fallback_chain.ainvoke({
            "topic": topic,
            "research_context": research_context
        })
        
        summary_text = fallback_result.content if hasattr(fallback_result, 'content') else str(fallback_result)
        
        logger.info(f"✅ Generated fallback summary: {len(summary_text)} chars")
        
        return {
            "summary": summary_text,
            "key_findings": [],
            "citations": []
        }
