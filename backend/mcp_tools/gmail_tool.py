"""Gmail MCP tool wrapper for sending emails."""
import os
from typing import Dict, Any
from langchain.tools import tool
from .mcp_client import MCPClient, MCPHTTPClient


class GmailMCPTool:
    """Gmail MCP tool wrapper."""
    
    def __init__(
        self,
        credentials_path: str = None,
        token_path: str = None,
        use_http: bool = False,
        http_url: str = None
    ):
        """
        Initialize Gmail MCP tool.
        
        Args:
            credentials_path: Path to credentials.json
            token_path: Path to token.json
            use_http: Whether to use HTTP wrapper (for Railway)
            http_url: HTTP wrapper URL (if use_http=True)
        """
        self.credentials_path = credentials_path or os.getenv(
            "GMAIL_CREDENTIALS_PATH",
            "./mcp_servers/gmail/credentials.json"
        )
        self.token_path = token_path or os.getenv(
            "GMAIL_TOKEN_PATH",
            "./mcp_servers/gmail/token.json"
        )
        self.use_http = use_http
        self.http_url = http_url or os.getenv("GMAIL_MCP_URL", "http://localhost:3001")
        
    async def send_email(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        """
        Send email via Gmail MCP.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (HTML or plain text)
            
        Returns:
            Result with email ID
        """
        if self.use_http:
            client = MCPHTTPClient(self.http_url)
        else:
            client = MCPClient(
                command="npx",
                args=["-y", "@modelcontextprotocol/server-gmail"],
                env={
                    "GMAIL_CREDENTIALS_PATH": self.credentials_path,
                    "GMAIL_TOKEN_PATH": self.token_path
                }
            )
        
        result = await client.call_tool("send_email", {
            "to": to,
            "subject": subject,
            "body": body
        })
        
        return result


# LangChain tool wrapper
@tool
async def send_research_email(to: str, subject: str, body: str) -> str:
    """
    Send research summary email via Gmail.
    
    Args:
        to: Recipient email address
        subject: Email subject line
        body: Email body (HTML or plain text)
    
    Returns:
        Success message with email ID
    """
    gmail = GmailMCPTool()
    result = await gmail.send_email(to, subject, body)
    
    # Extract email ID from result
    email_id = result.get("id", "unknown") if isinstance(result, dict) else "unknown"
    
    return f"✅ Email sent successfully to {to}. Message ID: {email_id}"
