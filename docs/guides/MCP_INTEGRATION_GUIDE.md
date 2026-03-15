# MCP INTEGRATION GUIDE

**Complete Guide to Model Context Protocol Integration for Research Agent**

---

## 📖 What is MCP?

**Model Context Protocol (MCP)** is an open standard that enables AI models to securely interact with external data sources and tools through a standardized interface.

### Key Concepts
- **MCP Server**: External service that provides tools/resources (e.g., Gmail, web search)
- **MCP Client**: Application that connects to MCP servers (our Python backend)
- **Transport**: Communication method (stdio, SSE, HTTP)
- **Tools**: Functions exposed by MCP servers (e.g., `send_email`, `web_search`)
- **Resources**: Static data provided by servers (e.g., file contents, database records)

### Why MCP for This Project?
- ✅ Standardized way to integrate Gmail and web search
- ✅ Secure OAuth handling by MCP server
- ✅ Official servers maintained by Anthropic/community
- ✅ Future-proof: Add more MCP servers easily

---

## 🔧 MCP Servers Used

### 1. Gmail MCP Server
**Package**: `@modelcontextprotocol/server-gmail`  
**Purpose**: Send emails via Gmail API with OAuth2 authentication  
**Transport**: stdio (local), HTTP (Railway)

**Tools Provided**:
- `send_email(to, subject, body)` - Send email
- `search_emails(query)` - Search inbox (optional)
- `get_email(id)` - Retrieve email (optional)

**Authentication**: OAuth2 with credentials.json + token.json

---

### 2. Brave Search MCP Server
**Package**: `@modelcontextprotocol/server-brave-search`  
**Purpose**: Web search using Brave Search API  
**Transport**: stdio (local), HTTP (Railway)

**Tools Provided**:
- `web_search(query, count)` - Search web and return results

**Authentication**: Brave API key (free tier: 2000 queries/month)

---

## 🚀 Gmail MCP Setup (Step-by-Step)

### Prerequisites
- Google account
- Node.js 18+ installed
- 45-60 minutes for first-time setup

### Step 1: Google Cloud Console Setup

1. **Go to Google Cloud Console**:
   - Visit: https://console.cloud.google.com
   - Sign in with your Google account

2. **Create New Project**:
   ```
   - Click "Select a project" → "New Project"
   - Project name: "MCP Research Agent"
   - Click "Create"
   ```

3. **Enable Gmail API**:
   ```
   - Navigate to "APIs & Services" → "Library"
   - Search for "Gmail API"
   - Click "Enable"
   ```

4. **Configure OAuth Consent Screen**:
   ```
   - Go to "APIs & Services" → "OAuth consent screen"
   - User Type: "External" (for testing)
   - Click "Create"
   
   App Information:
   - App name: "MCP Research Agent"
   - User support email: your-email@gmail.com
   - Developer contact: your-email@gmail.com
   - Click "Save and Continue"
   
   Scopes:
   - Click "Add or Remove Scopes"
   - Add: "https://www.googleapis.com/auth/gmail.send"
   - Add: "https://www.googleapis.com/auth/gmail.readonly" (optional)
   - Click "Update" → "Save and Continue"
   
   Test Users:
   - Click "Add Users"
   - Add your Gmail address
   - Click "Save and Continue"
   ```

5. **Create OAuth Credentials**:
   ```
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "MCP Gmail Client"
   - Click "Create"
   - Download credentials.json
   ```

### Step 2: Local Gmail MCP Setup

1. **Create MCP directory**:
   ```bash
   cd /Volumes/WorkSpace/Projects/InterviewPreps/MCPAIResearchAgent
   mkdir -p mcp_servers/gmail
   cd mcp_servers/gmail
   ```

2. **Move credentials.json**:
   ```bash
   # Move downloaded credentials.json to mcp_servers/gmail/
   mv ~/Downloads/credentials.json .
   ```

3. **Run OAuth Flow** (generates token.json):
   ```bash
   npx -y @modelcontextprotocol/server-gmail
   ```
   
   **What happens**:
   - Opens browser for Google OAuth
   - Select your Google account
   - Click "Allow" for Gmail permissions
   - Browser shows "Authentication successful"
   - `token.json` is created automatically

4. **Verify Files**:
   ```bash
   ls -la
   # Should see:
   # - credentials.json
   # - token.json
   ```

5. **Test Gmail MCP**:
   ```bash
   # Test sending email
   echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"send_email","arguments":{"to":"your-email@gmail.com","subject":"Test from MCP","body":"Hello from Gmail MCP!"}}}' | npx -y @modelcontextprotocol/server-gmail
   ```

### Step 3: Secure Token Storage

**CRITICAL**: Never commit credentials.json or token.json to git!

1. **Add to .gitignore**:
   ```bash
   # In project root
   echo "mcp_servers/gmail/credentials.json" >> .gitignore
   echo "mcp_servers/gmail/token.json" >> .gitignore
   echo "mcp_servers/gmail/*.json" >> .gitignore
   ```

2. **Backup tokens** (encrypted):
   ```bash
   # Store in password manager or encrypted vault
   # For Railway deployment, we'll use PostgreSQL
   ```

---

## 🔍 Brave Search MCP Setup

### Step 1: Get Brave API Key

1. **Sign up for Brave Search API**:
   - Visit: https://brave.com/search/api/
   - Click "Get Started"
   - Sign up with email
   - Verify email

2. **Create API Key**:
   - Go to dashboard
   - Click "Create API Key"
   - Name: "MCP Research Agent"
   - Copy API key (starts with `BSA...`)

3. **Store API Key**:
   ```bash
   # Add to .env file
   echo "BRAVE_API_KEY=BSA_your_key_here" >> .env
   ```

### Step 2: Test Brave Search MCP

```bash
# Set environment variable
export BRAVE_API_KEY="BSA_your_key_here"

# Test search
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"web_search","arguments":{"query":"latest AI developments","count":5}}}' | npx -y @modelcontextprotocol/server-brave-search
```

---

## 🐍 Python MCP Client Integration

### Install MCP Python Package

```bash
cd backend
pip install mcp anthropic langchain langchain-anthropic
```

### MCP Client Base Class

**File**: `backend/mcp_tools/mcp_client.py`

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from typing import Any, Dict, List

class MCPClient:
    """Base class for MCP server connections"""
    
    def __init__(self, server_command: str, server_args: List[str], env: Dict[str, str] = None):
        self.server_params = StdioServerParameters(
            command=server_command,
            args=server_args,
            env=env or {}
        )
        self.session = None
    
    async def __aenter__(self):
        """Start MCP server connection"""
        self.session = ClientSession(self.server_params)
        await self.session.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close MCP server connection"""
        if self.session:
            await self.session.__aexit__(exc_type, exc_val, exc_tb)
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call MCP tool with arguments"""
        if not self.session:
            raise RuntimeError("MCP session not initialized. Use 'async with' context.")
        
        result = await self.session.call_tool(tool_name, arguments)
        return result.content
    
    async def list_tools(self) -> List[str]:
        """List available tools from MCP server"""
        if not self.session:
            raise RuntimeError("MCP session not initialized.")
        
        tools = await self.session.list_tools()
        return [tool.name for tool in tools]
```

---

## 📧 Gmail MCP Tool Wrapper

**File**: `backend/mcp_tools/gmail_tool.py`

```python
import os
from typing import Dict, Any
from langchain.tools import tool
from .mcp_client import MCPClient

class GmailMCPTool:
    """Gmail MCP tool wrapper for LangChain"""
    
    def __init__(self, credentials_path: str = None, token_path: str = None):
        self.credentials_path = credentials_path or os.getenv(
            "GMAIL_CREDENTIALS_PATH",
            "./mcp_servers/gmail/credentials.json"
        )
        self.token_path = token_path or os.getenv(
            "GMAIL_TOKEN_PATH",
            "./mcp_servers/gmail/token.json"
        )
    
    async def send_email(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        """Send email via Gmail MCP"""
        async with MCPClient(
            server_command="npx",
            server_args=["-y", "@modelcontextprotocol/server-gmail"],
            env={
                "GMAIL_CREDENTIALS_PATH": self.credentials_path,
                "GMAIL_TOKEN_PATH": self.token_path
            }
        ) as client:
            result = await client.call_tool("send_email", {
                "to": to,
                "subject": subject,
                "body": body
            })
            return result

# LangChain tool decorator
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
    return f"Email sent successfully to {to}. Message ID: {result.get('id', 'unknown')}"
```

---

## 🔍 Search MCP Tool Wrapper

**File**: `backend/mcp_tools/search_tool.py`

```python
import os
from typing import List, Dict, Any
from langchain.tools import tool
from .mcp_client import MCPClient

class SearchMCPTool:
    """Brave Search MCP tool wrapper"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("BRAVE_API_KEY")
        if not self.api_key:
            raise ValueError("BRAVE_API_KEY not set")
    
    async def web_search(self, query: str, count: int = 5) -> List[Dict[str, Any]]:
        """Search web via Brave Search MCP"""
        async with MCPClient(
            server_command="npx",
            server_args=["-y", "@modelcontextprotocol/server-brave-search"],
            env={"BRAVE_API_KEY": self.api_key}
        ) as client:
            result = await client.call_tool("web_search", {
                "query": query,
                "count": count
            })
            return result

# LangChain tool decorator
@tool
async def search_web(query: str, max_results: int = 5) -> str:
    """
    Search the web for information.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 5)
    
    Returns:
        JSON string with search results including titles, URLs, and snippets
    """
    search = SearchMCPTool()
    results = await search.web_search(query, max_results)
    
    # Format results for LLM consumption
    formatted = []
    for i, result in enumerate(results, 1):
        formatted.append(f"""
Result {i}:
Title: {result.get('title', 'N/A')}
URL: {result.get('url', 'N/A')}
Snippet: {result.get('description', 'N/A')}
""")
    
    return "\n".join(formatted)
```

---

## 🧪 Testing MCP Tools

### Unit Test for Gmail Tool

**File**: `tests/test_mcp_tools.py`

```python
import pytest
import asyncio
from backend.mcp_tools.gmail_tool import GmailMCPTool

@pytest.mark.asyncio
async def test_gmail_send():
    """Test Gmail MCP email sending"""
    gmail = GmailMCPTool()
    
    result = await gmail.send_email(
        to="test@example.com",
        subject="Test Email",
        body="This is a test email from MCP integration test."
    )
    
    assert result is not None
    assert "id" in result or "success" in result

@pytest.mark.asyncio
async def test_search_tool():
    """Test Brave Search MCP"""
    from backend.mcp_tools.search_tool import SearchMCPTool
    
    search = SearchMCPTool()
    results = await search.web_search("Python programming", count=3)
    
    assert len(results) > 0
    assert "title" in results[0]
    assert "url" in results[0]
```

---

## 🐳 MCP HTTP Wrapper for Railway

Since Railway expects HTTP services, we need to wrap MCP stdio servers.

### Gmail MCP HTTP Wrapper

**File**: `mcp_servers/gmail/server.ts`

```typescript
import express from 'express';
import { spawn } from 'child_process';
import { v4 as uuidv4 } from 'uuid';

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3001;

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'gmail-mcp' });
});

// MCP tool call endpoint
app.post('/mcp/call', async (req, res) => {
  const { tool, arguments: args } = req.body;
  
  if (!tool || !args) {
    return res.status(400).json({ error: 'Missing tool or arguments' });
  }
  
  try {
    // Spawn MCP server process
    const mcpProcess = spawn('npx', ['-y', '@modelcontextprotocol/server-gmail'], {
      env: {
        ...process.env,
        GMAIL_CREDENTIALS_PATH: process.env.GMAIL_CREDENTIALS_PATH || './credentials.json',
        GMAIL_TOKEN_PATH: process.env.GMAIL_TOKEN_PATH || './token.json'
      }
    });
    
    // Prepare JSON-RPC request
    const request = {
      jsonrpc: '2.0',
      id: uuidv4(),
      method: 'tools/call',
      params: {
        name: tool,
        arguments: args
      }
    };
    
    let responseData = '';
    
    // Handle stdout
    mcpProcess.stdout.on('data', (data) => {
      responseData += data.toString();
    });
    
    // Handle stderr
    mcpProcess.stderr.on('data', (data) => {
      console.error('MCP Error:', data.toString());
    });
    
    // Handle process completion
    mcpProcess.on('close', (code) => {
      if (code === 0) {
        try {
          const result = JSON.parse(responseData);
          res.json(result);
        } catch (e) {
          res.status(500).json({ error: 'Failed to parse MCP response' });
        }
      } else {
        res.status(500).json({ error: `MCP process exited with code ${code}` });
      }
    });
    
    // Send request to MCP server
    mcpProcess.stdin.write(JSON.stringify(request) + '\n');
    mcpProcess.stdin.end();
    
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Gmail MCP HTTP wrapper listening on port ${PORT}`);
});
```

### Dockerfile for Gmail MCP

**File**: `mcp_servers/gmail/Dockerfile`

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Install dependencies
RUN npm install -g @modelcontextprotocol/server-gmail express uuid

# Copy server wrapper
COPY server.ts .

# Expose port
EXPOSE 3001

# Start server
CMD ["npx", "tsx", "server.ts"]
```

---

## 🔄 Using MCP Tools in Agents

### Example: Email Sender Agent

**File**: `backend/agents/email_sender.py`

```python
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate
from backend.mcp_tools.gmail_tool import send_research_email

async def send_research_via_email(summary: str, client_email: str, topic: str) -> dict:
    """Send research summary via Gmail MCP"""
    
    # Initialize Claude
    llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)
    
    # Create agent with Gmail tool
    tools = [send_research_email]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an email assistant. Format the research summary as a professional email."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    
    # Execute
    result = await executor.ainvoke({
        "input": f"Send this research summary about '{topic}' to {client_email}:\n\n{summary}"
    })
    
    return result
```

---

## 🚨 Common Issues & Troubleshooting

### Issue 1: "OAuth token expired"
**Solution**:
```python
# Token refresh is automatic in MCP server
# If fails, delete token.json and re-run OAuth flow
rm mcp_servers/gmail/token.json
npx -y @modelcontextprotocol/server-gmail
```

### Issue 2: "BRAVE_API_KEY not found"
**Solution**:
```bash
# Ensure .env is loaded
export BRAVE_API_KEY="your_key_here"
# Or use python-dotenv
pip install python-dotenv
```

### Issue 3: "MCP server not responding"
**Solution**:
```python
# Check if Node.js is installed
node --version  # Should be 18+

# Test MCP server manually
npx -y @modelcontextprotocol/server-gmail
```

### Issue 4: "Permission denied on Railway"
**Solution**:
```bash
# Store tokens in PostgreSQL instead of filesystem
# See DOCKER_RAILWAY_DEPLOYMENT.md for details
```

---

## 📚 Additional Resources

- **MCP Specification**: https://modelcontextprotocol.io/
- **Gmail MCP Server**: https://github.com/modelcontextprotocol/servers/tree/main/src/gmail
- **Brave Search API**: https://brave.com/search/api/docs
- **LangChain MCP Integration**: https://python.langchain.com/docs/integrations/tools/

---

**Next Steps**: See `LANGGRAPH_WORKFLOW.md` for integrating these tools into the agent workflow.
