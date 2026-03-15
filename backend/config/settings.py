"""Application settings and configuration."""
from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

# Get the directory where this settings.py file is located
BACKEND_DIR = Path(__file__).parent.parent
ENV_FILE = BACKEND_DIR / ".env"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    anthropic_api_key: str
    tavily_api_key: str  # Free tier: 1000 searches/month
    langsmith_api_key: Optional[str] = None
    
    # LangSmith Configuration
    langsmith_project: str = "mcp-research-agent"
    langsmith_tracing_v2: bool = True
    
    # Gmail MCP Configuration
    gmail_credentials_path: str = "./mcp_servers/gmail/credentials.json"
    gmail_token_path: str = "./mcp_servers/gmail/token.json"
    
    # MCP Server URLs (for Railway deployment)
    gmail_mcp_url: str = "http://localhost:3001"
    search_mcp_url: str = "http://localhost:3002"
    
    # Database
    database_url: str = "sqlite:///./data/research_agent.db"
    
    # Redis (optional)
    redis_url: Optional[str] = None
    
    # Application Settings
    environment: str = "development"
    debug: bool = True
    max_sub_queries: int = 5
    max_retry_attempts: int = 2
    request_timeout: int = 120
    
    # Feature Flags
    email_enabled: bool = False  # Enable/disable email functionality
    
    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    class Config:
        env_file = str(ENV_FILE)
        case_sensitive = False


# Global settings instance
settings = Settings()
