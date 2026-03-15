"""Logging configuration for MCP Research Agent."""
import logging
import sys
from pathlib import Path
import os

# Create logs directory (handle permission errors gracefully)
LOGS_DIR = Path(__file__).parent.parent / "logs"
try:
    LOGS_DIR.mkdir(exist_ok=True)
    LOGS_ENABLED = True
except (PermissionError, OSError) as e:
    # If we can't create logs directory (e.g., in production), disable file logging
    print(f"Warning: Cannot create logs directory: {e}. File logging disabled.")
    LOGS_ENABLED = False

def setup_logging(debug: bool = True):
    """
    Setup comprehensive logging for the application.
    
    Args:
        debug: Enable debug level logging
    """
    # Root logger configuration
    log_level = logging.DEBUG if debug else logging.INFO
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(levelname)-8s | %(message)s'
    )
    
    # Console handler (simple format)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(simple_formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # Add file handlers only if logs directory is available
    if LOGS_ENABLED:
        # File handler (detailed format)
        file_handler = logging.FileHandler(LOGS_DIR / "research_agent.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(file_handler)
        
        # Agent-specific file handler
        agent_handler = logging.FileHandler(LOGS_DIR / "agents.log")
        agent_handler.setLevel(logging.DEBUG)
        agent_handler.setFormatter(detailed_formatter)
        
        # Workflow file handler
        workflow_handler = logging.FileHandler(LOGS_DIR / "workflow.log")
        workflow_handler.setLevel(logging.DEBUG)
        workflow_handler.setFormatter(detailed_formatter)
        
        # Configure agent loggers
        for agent in ['planner', 'retriever', 'summarizer', 'verifier', 'email_sender']:
            agent_logger = logging.getLogger(f'agents.{agent}')
            agent_logger.addHandler(agent_handler)
            agent_logger.setLevel(logging.DEBUG)
        
        # Configure workflow logger
        workflow_logger = logging.getLogger('graph.workflow')
        workflow_logger.addHandler(workflow_handler)
        workflow_logger.setLevel(logging.DEBUG)
    
    # Suppress noisy libraries
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    if LOGS_ENABLED:
        logging.info("🚀 Logging system initialized (console + file)")
        logging.info(f"📁 Log files location: {LOGS_DIR}")
    else:
        logging.info("🚀 Logging system initialized (console only)")
    logging.info(f"🔍 Debug mode: {debug}")


def get_agent_logger(agent_name: str) -> logging.Logger:
    """
    Get a logger for a specific agent.
    
    Args:
        agent_name: Name of the agent (planner, retriever, etc.)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(f'agents.{agent_name}')


def get_workflow_logger() -> logging.Logger:
    """Get the workflow logger."""
    return logging.getLogger('graph.workflow')
