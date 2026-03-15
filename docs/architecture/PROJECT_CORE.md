# PROJECT CORE - MCP Multi-Agent Research System

**Single Source of Truth for Architecture, Tech Stack, and Design Decisions**

---

## 🎯 Project Mission

Build a production-ready multi-agent AI system that:
1. Accepts a research topic and client email from users
2. Autonomously plans, researches, synthesizes, and verifies information
3. Sends polished research summaries via email using MCP (Model Context Protocol)
4. Demonstrates real-world MCP integration and LangGraph orchestration
5. Deploys to Railway using Docker containers

**Learning Goals**:
- Master MCP protocol integration (Gmail, Web Search)
- Implement multi-agent workflows with LangGraph
- Build production-grade guardrails and verification
- Deploy containerized AI agents to cloud infrastructure

---

## 🏗️ System Architecture

### High-Level Flow
```
┌─────────────┐
│   User UI   │ (React + Vite)
│ - Topic     │
│ - Email     │
└──────┬──────┘
       │ HTTP POST
       ▼
┌─────────────────────────────────────────┐
│         FastAPI Backend                 │
│  ┌───────────────────────────────────┐  │
│  │      LangGraph Workflow           │  │
│  │                                   │  │
│  │  ┌─────────────┐                 │  │
│  │  │  PLANNER    │ ← Claude Sonnet │  │
│  │  └──────┬──────┘                 │  │
│  │         │ Sub-queries            │  │
│  │         ▼                         │  │
│  │  ┌─────────────┐                 │  │
│  │  │  RETRIEVER  │ ← MCP Search    │  │
│  │  └──────┬──────┘                 │  │
│  │         │ Raw data               │  │
│  │         ▼                         │  │
│  │  ┌─────────────┐                 │  │
│  │  │ SUMMARIZER  │ ← Claude Sonnet │  │
│  │  └──────┬──────┘                 │  │
│  │         │ Draft                  │  │
│  │         ▼                         │  │
│  │  ┌─────────────┐                 │  │
│  │  │  VERIFIER   │ ← Claude + Eval │  │
│  │  └──────┬──────┘                 │  │
│  │         │ Pass/Fail              │  │
│  │         ▼                         │  │
│  │  ┌─────────────┐                 │  │
│  │  │ GUARDRAILS  │ ← Pydantic +    │  │
│  │  │             │   LlamaGuard    │  │
│  │  └──────┬──────┘                 │  │
│  │         │ Clean output           │  │
│  │         ▼                         │  │
│  │  ┌─────────────┐                 │  │
│  │  │ EMAIL SENDER│ ← Gmail MCP     │  │
│  │  └─────────────┘                 │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
       │ SSE Stream (status updates)
       ▼
┌─────────────┐
│   User UI   │ (Real-time progress)
└─────────────┘
```

### MCP Integration Points
```
┌──────────────────────────────────────────┐
│         MCP Servers (External)           │
├──────────────────────────────────────────┤
│                                          │
│  ┌────────────────┐  ┌────────────────┐ │
│  │  Gmail MCP     │  │  Search MCP    │ │
│  │  (Node.js)     │  │  (Node.js)     │ │
│  │                │  │                │ │
│  │ - send_email   │  │ - web_search   │ │
│  │ - OAuth2       │  │ - Brave API    │ │
│  └────────┬───────┘  └────────┬───────┘ │
│           │                   │          │
└───────────┼───────────────────┼──────────┘
            │ stdio/HTTP        │
            ▼                   ▼
┌──────────────────────────────────────────┐
│      Python Backend (MCP Client)         │
│  - mcp Python package                    │
│  - LangChain tool wrappers               │
└──────────────────────────────────────────┘
```

---

## 📦 Complete Tech Stack

### Backend (Python 3.12)
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Orchestration** | LangGraph | ^0.2.0 | Multi-agent workflow state machine |
| **LLM Framework** | LangChain | ^0.3.0 | Agent framework and tool integration |
| **LLM Provider** | Anthropic Claude | Sonnet 4 | Primary reasoning engine |
| **API Framework** | FastAPI | ^0.115.0 | REST API and SSE endpoints |
| **MCP Client** | mcp | ^1.0.0 | Model Context Protocol client |
| **Validation** | Pydantic | ^2.0 | Schema validation and type safety |
| **Guardrails** | LlamaGuard | ^0.1.0 | Content safety filtering |
| **Observability** | LangSmith | Latest | Tracing and evaluation |
| **Database** | SQLite | Built-in | LangGraph checkpointing (local) |
| **Database (Prod)** | PostgreSQL | 15 | State persistence on Railway |
| **Caching** | Redis | 7 | Search result caching (optional) |
| **Server** | Uvicorn | ^0.30.0 | ASGI server |

### Frontend (React + TypeScript)
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | React | ^18.3.0 | UI framework |
| **Language** | TypeScript | ^5.5.0 | Type safety |
| **Build Tool** | Vite | ^5.4.0 | Fast dev server and bundler |
| **UI Library** | Shadcn/ui | Latest | Accessible component library |
| **Styling** | TailwindCSS | ^3.4.0 | Utility-first CSS |
| **Icons** | Lucide React | ^0.400.0 | Icon library |
| **State** | React Query | ^5.0.0 | Server state management |
| **Forms** | React Hook Form | ^7.52.0 | Form validation |
| **Validation** | Zod | ^3.23.0 | Schema validation |

### MCP Servers (Node.js)
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Gmail MCP** | @modelcontextprotocol/server-gmail | Email sending via OAuth2 |
| **Search MCP** | @modelcontextprotocol/server-brave-search | Web search via Brave API |
| **Custom MCP** | fastmcp | Custom data sources (optional) |

### DevOps & Deployment
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Containerization** | Docker | Multi-container deployment |
| **Orchestration** | Docker Compose | Local development |
| **Cloud Platform** | Railway | Production hosting |
| **CI/CD** | GitHub Actions | Automated deployment |
| **Secrets** | Railway Secrets | Environment variable management |

---

## 🔑 Key Design Decisions

### 1. **LangGraph over LangChain LCEL**
**Decision**: Use LangGraph for workflow orchestration instead of LangChain Expression Language.

**Rationale**:
- ✅ Explicit state management with TypedDict
- ✅ Built-in checkpointing for long-running workflows
- ✅ Conditional routing based on verification results
- ✅ Better observability with LangSmith
- ✅ Easier to debug and test individual nodes

**Trade-off**: Slightly more boilerplate than LCEL chains.

---

### 2. **Multi-Container Architecture for Railway**
**Decision**: Separate Docker containers for backend, Gmail MCP, and Search MCP.

**Rationale**:
- ✅ Railway's multi-service support handles networking
- ✅ Independent scaling of MCP servers
- ✅ Easier to debug and update individual services
- ✅ MCP servers need HTTP wrappers anyway (stdio → HTTP)

**Trade-off**: More complex deployment configuration than monolithic container.

---

### 3. **PostgreSQL for Token Storage**
**Decision**: Store Gmail OAuth tokens in Railway PostgreSQL, not filesystem.

**Rationale**:
- ✅ Railway has ephemeral filesystem
- ✅ Tokens persist across deployments
- ✅ Can encrypt tokens at rest
- ✅ Automatic refresh token rotation

**Trade-off**: Requires database setup and encryption logic.

---

### 4. **Claude Sonnet 4 as Primary LLM**
**Decision**: Use Claude Sonnet 4 for all agent reasoning (Planner, Summarizer, Verifier).

**Rationale**:
- ✅ Best-in-class reasoning capabilities
- ✅ Long context window (200K tokens)
- ✅ Strong citation and factual accuracy
- ✅ Native MCP support in Anthropic SDK

**Trade-off**: Higher cost than GPT-3.5, but necessary for quality.

---

### 5. **SSE over WebSockets for Status Streaming**
**Decision**: Use Server-Sent Events (SSE) instead of WebSockets.

**Rationale**:
- ✅ Simpler implementation (one-way communication)
- ✅ Built-in reconnection in EventSource API
- ✅ Works with Railway's HTTP routing
- ✅ No need for WebSocket library

**Trade-off**: Can't send messages from client to server mid-stream (not needed here).

---

### 6. **Pydantic + LlamaGuard for Guardrails**
**Decision**: Two-layer guardrail system.

**Rationale**:
- ✅ Pydantic: Structural validation (schema, types, required fields)
- ✅ LlamaGuard: Content safety (harmful content, hallucinations)
- ✅ Complementary strengths
- ✅ Fast fail on structural issues before expensive LLM checks

**Trade-off**: Two validation steps add latency (~200ms).

---

### 7. **Minimal UI with Shadcn/ui**
**Decision**: Simple form + status stream, no complex features.

**Rationale**:
- ✅ Focus on backend/MCP integration learning
- ✅ Shadcn/ui provides accessible components out-of-box
- ✅ TailwindCSS for rapid styling
- ✅ Can add features later (history, editing, etc.)

**Trade-off**: Limited UX features in v1.

---

## 📊 Data Flow & State Management

### LangGraph State Schema
```python
from typing import TypedDict, List, Dict, Optional

class ResearchState(TypedDict):
    # User inputs
    topic: str
    client_email: str
    
    # Planner outputs
    research_plan: Dict[str, any]  # Structured plan with sub-queries
    sub_queries: List[str]
    
    # Retriever outputs
    raw_data: List[Dict[str, any]]  # Search results with metadata
    sources: List[str]  # URLs for citation
    
    # Summarizer outputs
    summary: str
    citations: List[Dict[str, str]]
    
    # Verifier outputs
    verification_status: str  # "pass" | "fail" | "needs_revision"
    verification_feedback: Optional[str]
    
    # Final outputs
    final_output: str
    email_sent: bool
    email_timestamp: Optional[str]
    
    # Metadata
    workflow_id: str
    current_step: str
    errors: List[str]
    retry_count: int
```

### State Transitions
```
INIT → PLANNING → RETRIEVING → SUMMARIZING → VERIFYING
                                                  ↓
                                            [Pass/Fail?]
                                                  ↓
                                    Pass → SENDING_EMAIL → COMPLETE
                                                  ↓
                                    Fail → SUMMARIZING (retry)
                                           (max 2 retries)
```

---

## 🎯 Success Criteria

### Functional Requirements
- [ ] User can submit topic + email via UI
- [ ] System generates 3-5 sub-queries from topic
- [ ] MCP web search retrieves relevant sources
- [ ] Summary includes proper citations
- [ ] Verifier catches at least one hallucination in testing
- [ ] Email sent successfully via Gmail MCP
- [ ] Real-time status updates stream to UI
- [ ] Workflow recovers from at least one error scenario

### Non-Functional Requirements
- [ ] End-to-end workflow completes in <2 minutes (typical topic)
- [ ] LangSmith traces show all agent steps
- [ ] UI is responsive on mobile and desktop
- [ ] Docker containers build successfully
- [ ] Railway deployment completes without errors
- [ ] Cost per research: <$0.50 (Claude API + search)

### Quality Requirements
- [ ] 90%+ test coverage for agents
- [ ] Zero security vulnerabilities in dependencies
- [ ] All API endpoints have error handling
- [ ] Guardrails prevent inappropriate content
- [ ] OAuth tokens stored securely (encrypted)

---

## 📁 Project Structure Reference

```
MCPAIResearchAgent/
├── docs/                           # Knowledge base (this file)
│   ├── PROJECT_CORE.md            # ← You are here
│   ├── MCP_INTEGRATION_GUIDE.md
│   ├── LANGGRAPH_WORKFLOW.md
│   ├── AGENT_SPECIFICATIONS.md
│   ├── DOCKER_RAILWAY_DEPLOYMENT.md
│   └── DEVELOPMENT_SETUP.md
│
├── backend/                        # Python backend
│   ├── agents/                     # Individual agent implementations
│   │   ├── __init__.py
│   │   ├── planner.py
│   │   ├── retriever.py
│   │   ├── summarizer.py
│   │   ├── verifier.py
│   │   └── email_sender.py
│   │
│   ├── graph/                      # LangGraph workflow
│   │   ├── __init__.py
│   │   ├── state.py               # ResearchState TypedDict
│   │   └── workflow.py            # LangGraph state machine
│   │
│   ├── mcp_tools/                  # MCP integrations
│   │   ├── __init__.py
│   │   ├── gmail_tool.py          # Gmail MCP wrapper
│   │   ├── search_tool.py         # Search MCP wrapper
│   │   └── mcp_client.py          # Base MCP client
│   │
│   ├── guardrails/                 # Validation & safety
│   │   ├── __init__.py
│   │   ├── validators.py          # Pydantic models
│   │   └── content_safety.py      # LlamaGuard integration
│   │
│   ├── api/                        # FastAPI application
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI app
│   │   ├── routes.py              # Endpoints
│   │   └── sse.py                 # Server-Sent Events
│   │
│   ├── config/                     # Configuration
│   │   ├── __init__.py
│   │   ├── settings.py            # Environment variables
│   │   └── mcp_config.json        # MCP server configs
│   │
│   ├── Dockerfile                  # Backend container
│   └── requirements.txt            # Python dependencies
│
├── frontend/                       # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── ResearchForm.tsx   # Topic + email input
│   │   │   ├── StatusStream.tsx   # Real-time progress
│   │   │   └── ResultDisplay.tsx  # Final summary
│   │   ├── lib/
│   │   │   ├── api.ts             # Backend API client
│   │   │   └── utils.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── mcp_servers/                    # MCP server configurations
│   ├── gmail/
│   │   ├── Dockerfile             # Gmail MCP container
│   │   ├── server.ts              # HTTP wrapper
│   │   ├── credentials.json       # (gitignored)
│   │   └── token.json             # (gitignored)
│   └── search/
│       ├── Dockerfile             # Search MCP container
│       └── server.ts              # HTTP wrapper
│
├── tests/                          # Test suite
│   ├── test_agents.py
│   ├── test_workflow.py
│   ├── test_mcp_tools.py
│   └── test_api.py
│
├── .env.example                    # Environment template
├── .gitignore
├── docker-compose.yml              # Local development
├── railway.json                    # Railway config
└── README.md
```

---

## 🔐 Security Considerations

### Secrets Management
- **Never commit**: credentials.json, token.json, .env
- **Railway Secrets**: Store all API keys and tokens
- **Encryption**: Encrypt OAuth tokens in PostgreSQL
- **Rotation**: Implement token refresh logic

### Input Validation
- **Topic**: Max 500 chars, sanitize HTML
- **Email**: Validate format, check domain
- **Rate Limiting**: Max 10 requests/hour per IP

### Content Safety
- **LlamaGuard**: Filter harmful content
- **Pydantic**: Strict schema validation
- **Citation Verification**: Ensure sources exist

---

## 📈 Observability & Monitoring

### LangSmith Integration
- **Traces**: Every workflow execution
- **Evaluators**: Verify citation accuracy
- **Metrics**: Latency, cost, success rate
- **Alerts**: Failed workflows, high costs

### Logging Strategy
- **Structured Logs**: JSON format
- **Log Levels**: DEBUG (dev), INFO (prod)
- **Log Aggregation**: Railway logs dashboard

---

## 💰 Cost Estimation

### Per Research Workflow
| Component | Cost | Notes |
|-----------|------|-------|
| Claude API (Planner) | ~$0.05 | 1K input, 500 output tokens |
| Claude API (Summarizer) | ~$0.15 | 5K input, 1K output tokens |
| Claude API (Verifier) | ~$0.10 | 3K input, 500 output tokens |
| Brave Search API | ~$0.05 | 5 queries × $0.01 |
| Gmail API | Free | 250 emails/day limit |
| **Total per research** | **~$0.35** | Typical case |

### Monthly Costs (100 researches)
- Claude API: ~$35
- Brave Search: ~$5
- Railway: $5 (free tier credit)
- **Total**: ~$45/month

---

## 🚀 Next Steps

1. **Review this document** with team/stakeholders
2. **Create remaining knowledge base files** (MCP_INTEGRATION_GUIDE.md, etc.)
3. **Setup development environment** (Python 3.12, Node.js, Docker)
4. **Begin Phase 1**: Environment setup and Gmail MCP configuration

---

**Last Updated**: 2026-03-12  
**Version**: 1.0  
**Maintained By**: Development Team
