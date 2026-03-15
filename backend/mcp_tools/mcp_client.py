"""Base MCP client for communicating with MCP servers via subprocess."""
import asyncio
import json
import subprocess
from typing import Any, Dict, List, Optional
import uuid


class MCPClient:
    """Base class for MCP server communication via stdio."""
    
    def __init__(self, command: str, args: List[str], env: Optional[Dict[str, str]] = None):
        """
        Initialize MCP client.
        
        Args:
            command: Command to run MCP server (e.g., 'npx')
            args: Arguments for the command (e.g., ['-y', '@modelcontextprotocol/server-gmail'])
            env: Optional environment variables
        """
        self.command = command
        self.args = args
        self.env = env or {}
        
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call an MCP tool via subprocess.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments
            
        Returns:
            Tool result
        """
        # Prepare JSON-RPC request
        request = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        # Start MCP server process
        process = await asyncio.create_subprocess_exec(
            self.command,
            *self.args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={**self.env}
        )
        
        # Send request
        request_json = json.dumps(request) + '\n'
        stdout, stderr = await process.communicate(request_json.encode())
        
        # Parse response
        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Unknown error"
            raise RuntimeError(f"MCP server failed: {error_msg}")
        
        try:
            # MCP servers may return multiple JSON objects, get the last one
            response_lines = stdout.decode().strip().split('\n')
            for line in reversed(response_lines):
                if line.strip():
                    response = json.loads(line)
                    if "result" in response:
                        return response["result"]
                    elif "error" in response:
                        raise RuntimeError(f"MCP error: {response['error']}")
            
            raise RuntimeError("No valid response from MCP server")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse MCP response: {e}")


class MCPHTTPClient:
    """Client for MCP servers wrapped with HTTP (for Railway deployment)."""
    
    def __init__(self, base_url: str):
        """
        Initialize HTTP MCP client.
        
        Args:
            base_url: Base URL of the MCP HTTP wrapper
        """
        self.base_url = base_url.rstrip('/')
        
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call an MCP tool via HTTP.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments
            
        Returns:
            Tool result
        """
        import httpx
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/mcp/call",
                json={"tool": tool_name, "arguments": arguments},
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            
            if "error" in result:
                raise RuntimeError(f"MCP HTTP error: {result['error']}")
            
            return result.get("result", result)
