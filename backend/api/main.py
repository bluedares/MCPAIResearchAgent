"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import sys
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings
from api.routes import router as research_router
from utils.logger import setup_logging

# Setup logging
setup_logging(debug=settings.debug)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logging.info("🚀 Starting MCP Research Agent API...")
    logging.info(f"📍 Environment: {settings.environment}")
    logging.info(f"🔍 Debug mode: {settings.debug}")
    print("🚀 Starting MCP Research Agent API...")
    print(f"📍 Environment: {settings.environment}")
    print(f"🔍 Debug mode: {settings.debug}")
    
    # Create data directory if it doesn't exist
    os.makedirs("./data", exist_ok=True)
    
    # Initialize Redis cache
    from utils.redis_cache import init_redis
    init_redis()
    
    yield


# Create FastAPI app
app = FastAPI(
    title="MCP Research Agent API",
    description="Multi-agent AI research system using LangGraph and MCP",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(research_router, prefix="/api", tags=["research"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "MCP Research Agent API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "debug": settings.debug
    }


@app.get("/config")
async def get_config():
    """Get non-sensitive configuration."""
    return {
        "environment": settings.environment,
        "max_sub_queries": settings.max_sub_queries,
        "max_retry_attempts": settings.max_retry_attempts,
        "langsmith_enabled": settings.langsmith_api_key is not None,
        "redis_enabled": settings.redis_url is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
