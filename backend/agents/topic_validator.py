"""Topic validation agent to ensure research queries are appropriate."""
import logging
from typing import Dict, Any
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from config.settings import settings

logger = logging.getLogger(__name__)


class TopicValidation(BaseModel):
    """Topic validation result."""
    is_valid: bool = Field(description="Whether the topic is valid for research")
    reason: str = Field(description="Reason for validation decision")
    suggestion: str = Field(default="", description="Suggestion for improvement if invalid")


async def validate_topic(topic: str) -> Dict[str, Any]:
    """
    Validate if a topic is appropriate for research.
    
    Rejects:
    - Personal questions (e.g., "What is my name?", "Who am I?")
    - Too vague or short queries
    - Non-researchable questions
    - Inappropriate or offensive content
    - Questions requiring real-time personal data
    
    Args:
        topic: Research topic to validate
        
    Returns:
        Dictionary with validation result
    """
    logger.info(f"🔍 Validating topic: {topic[:100]}...")
    
    # Initialize Claude for validation
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0,
        api_key=settings.anthropic_api_key
    )
    
    # Use structured output for validation
    structured_llm = llm.with_structured_output(TopicValidation)
    
    # Validation prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a research topic validator. Analyze if the given topic is appropriate for web-based research.

**REJECT topics that are:**
1. **Personal questions** - Questions about the user's personal information (name, age, location, preferences, etc.)
   - Examples: "What is my name?", "Who am I?", "What do I like?", "Where do I live?"
   
2. **Too vague or short** - Less than 10 characters or extremely generic
   - Examples: "AI", "Technology", "News"
   
3. **Non-researchable** - Cannot be answered through web research
   - Examples: "What am I thinking?", "Predict my future", "Read my mind"
   
4. **Inappropriate content** - Offensive, harmful, or unethical requests
   
5. **Real-time personal data** - Requires access to user's private data
   - Examples: "What's in my email?", "Show my calendar", "My bank balance"

6. **Chunk/fragmented questions** - Incomplete sentences or random words
   - Examples: "the latest", "about that", "more info"

**ACCEPT topics that are:**
1. General knowledge research topics
2. Current events and news
3. Scientific or technical subjects
4. Historical topics
5. Industry trends and analysis
6. Product comparisons and reviews
7. How-to guides and tutorials

**Important:** When suggesting improvements, use 2026 as the current year in examples.

Respond with:
- is_valid: true/false
- reason: Brief explanation of why it's valid or invalid
- suggestion: If invalid, suggest how to improve the query (use 2026 for current year references)"""),
        ("human", "Topic to validate: {topic}")
    ])
    
    try:
        chain = prompt | structured_llm
        result = await chain.ainvoke({"topic": topic})
        
        if result.is_valid:
            logger.info(f"✅ Topic validated: {result.reason}")
        else:
            logger.warning(f"❌ Topic rejected: {result.reason}")
        
        return {
            "is_valid": result.is_valid,
            "reason": result.reason,
            "suggestion": result.suggestion
        }
        
    except Exception as e:
        logger.error(f"❌ Validation error: {e}")
        # On error, allow the topic (fail open for better UX)
        return {
            "is_valid": True,
            "reason": "Validation service unavailable, proceeding with research",
            "suggestion": ""
        }
