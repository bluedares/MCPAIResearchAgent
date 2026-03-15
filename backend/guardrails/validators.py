"""Pydantic validators for input validation and guardrails."""
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional


class TopicValidator(BaseModel):
    """Validate research topic input."""
    
    topic: str = Field(..., min_length=10, max_length=500)
    
    @validator('topic')
    def validate_topic(cls, v):
        """Validate topic is appropriate and not empty."""
        # Remove extra whitespace
        v = ' '.join(v.split())
        
        # Check for inappropriate content (basic filtering)
        inappropriate_keywords = ['hack', 'exploit', 'illegal', 'pirate']
        lower_topic = v.lower()
        
        for keyword in inappropriate_keywords:
            if keyword in lower_topic:
                raise ValueError(f"Topic contains inappropriate content: {keyword}")
        
        return v


class EmailValidator(BaseModel):
    """Validate email address."""
    
    email: EmailStr
    
    @validator('email')
    def validate_email_domain(cls, v):
        """Additional email validation."""
        # Could add domain whitelist/blacklist here
        return v


class ResearchOutputValidator(BaseModel):
    """Validate research output before sending."""
    
    summary: str = Field(..., min_length=100)
    citations: List[dict] = Field(..., min_items=1)
    
    @validator('summary')
    def validate_summary_length(cls, v):
        """Ensure summary is comprehensive."""
        word_count = len(v.split())
        if word_count < 50:
            raise ValueError("Summary too short - must be at least 50 words")
        return v
    
    @validator('citations')
    def validate_citations(cls, v):
        """Ensure all citations have required fields."""
        for citation in v:
            if 'source_url' not in citation or not citation['source_url']:
                raise ValueError("All citations must have a valid source_url")
            if 'claim' not in citation or not citation['claim']:
                raise ValueError("All citations must have a claim")
        return v


def validate_research_input(topic: str, email: str) -> tuple[str, str]:
    """
    Validate research input.
    
    Args:
        topic: Research topic
        email: Client email
        
    Returns:
        Validated (topic, email)
        
    Raises:
        ValueError: If validation fails
    """
    # Validate topic
    topic_validator = TopicValidator(topic=topic)
    validated_topic = topic_validator.topic
    
    # Validate email
    email_validator = EmailValidator(email=email)
    validated_email = email_validator.email
    
    return validated_topic, validated_email


def validate_research_output(summary: str, citations: List[dict]) -> bool:
    """
    Validate research output before sending.
    
    Args:
        summary: Research summary
        citations: List of citations
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If validation fails
    """
    validator = ResearchOutputValidator(summary=summary, citations=citations)
    return True
