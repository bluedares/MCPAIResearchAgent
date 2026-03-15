# PROJECT INDEX - Navigation Guide

**Quick reference to all documentation and project structure**

---

## 📚 Core Documentation (Read in Order)

### 1. **Start Here**
- **[README.md](../README.md)** - Project overview and quick start
- **[PROJECT_CORE.md](PROJECT_CORE.md)** - Architecture, tech stack, design decisions

### 2. **Setup & Configuration**
- **[DEVELOPMENT_SETUP.md](DEVELOPMENT_SETUP.md)** - Step-by-step local setup (30 min)
- **[MCP_INTEGRATION_GUIDE.md](MCP_INTEGRATION_GUIDE.md)** - Gmail & Search MCP setup
- **[TECH_STACK.md](TECH_STACK.md)** - Complete technology reference

### 3. **Implementation Guides** (Coming Next)
- **LANGGRAPH_WORKFLOW.md** - State machine implementation
- **AGENT_SPECIFICATIONS.md** - Individual agent details
- **GUARDRAILS_IMPLEMENTATION.md** - Safety & validation
- **API_CONTRACTS.md** - Backend API specs
- **FRONTEND_INTEGRATION.md** - React UI guide

### 4. **Deployment**
- **DOCKER_RAILWAY_DEPLOYMENT.md** - Production deployment guide

### 5. **Reference**
- **TESTING_STRATEGY.md** - Test coverage plan
- **COST_OPTIMIZATION.md** - Managing API costs
- **TROUBLESHOOTING.md** - Common issues & solutions

---

## 🗂️ Project Structure

```
MCPAIResearchAgent/
│
├── 📄 README.md                    ← Start here
├── 📄 .env.example                 ← Copy to .env
├── 📄 .gitignore                   ← Security (credentials excluded)
├── 📄 docker-compose.yml           ← Local multi-container setup
│
├── 📁 docs/                        ← Knowledge base
│   ├── PROJECT_INDEX.md           ← You are here
│   ├── PROJECT_CORE.md            ← Architecture & decisions
│   ├── MCP_INTEGRATION_GUIDE.md   ← MCP setup (critical!)
│   ├── TECH_STACK.md              ← All technologies used
│   └── DEVELOPMENT_SETUP.md       ← Quick start guide
│
├── 📁 backend/                     ← Python FastAPI + LangGraph
│   ├── Dockerfile                 ← Backend container
│   ├── requirements.txt           ← Python dependencies
│   ├── agents/                    ← To be created
│   ├── graph/                     ← To be created
│   ├── mcp_tools/                 ← To be created
│   ├── guardrails/                ← To be created
│   ├── api/                       ← To be created
│   └── config/                    ← To be created
│
├── 📁 frontend/                    ← React + TypeScript UI
│   ├── Dockerfile.dev             ← Frontend dev container
│   ├── package.json               ← Node dependencies
│   └── src/                       ← To be created
│       ├── components/            ← UI components
│       └── lib/                   ← API client
│
├── 📁 mcp_servers/                 ← MCP configurations
│   ├── gmail/                     ← Gmail MCP
│   │   ├── credentials.json       ← (gitignored - you create)
│   │   └── token.json             ← (gitignored - auto-created)
│   └── search/                    ← Search MCP
│
└── 📁 tests/                       ← Test suite (to be created)
```

---

## 🎯 UI Specifications

### User Input Form
1. **Research Topic** (textarea)
   - Min: 10 chars, Max: 500 chars
   - Example: "Latest developments in quantum computing"

2. **Client Email** (email input)
   - Valid email format required
   - Where research summary will be sent

3. **Submit Button**
   - Text: "Start Research"
   - Shows loading spinner during execution

### Real-Time Progress Display
```
🧠 Planning      ✅ (5-10s)
🔍 Researching   ⏳ (10-20s)
📝 Summarizing   ⏸️ (10-15s)
✅ Verifying     ⏸️ (5-10s)
📧 Sending       ⏸️ (2-5s)
```

### Result Display
- Summary preview (first 200 chars)
- Copy to clipboard button
- Email confirmation message
- Expandable full report

---

## 🚀 Quick Start Commands

### First-Time Setup
```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 2. Setup Gmail MCP (see MCP_INTEGRATION_GUIDE.md)
cd mcp_servers/gmail
npx -y @modelcontextprotocol/server-gmail

# 3. Install backend
cd ../../backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Install frontend
cd ../frontend
npm install
npx shadcn-ui@latest init
npx shadcn-ui@latest add button input textarea card progress alert badge
```

### Daily Development
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn api.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Open: http://localhost:5173
```

### Docker (Alternative)
```bash
docker-compose up --build
```

---

## 📋 Implementation Phases

### ✅ Phase 0: Foundation (COMPLETED)
- [x] Project structure created
- [x] Core documentation written
- [x] Configuration files ready
- [x] Docker setup complete

### 🔄 Phase 1: Environment Setup (NEXT)
- [ ] Configure .env with API keys
- [ ] Setup Gmail MCP OAuth
- [ ] Install backend dependencies
- [ ] Install frontend dependencies
- [ ] Test basic connectivity

### 📝 Phase 2: MCP Integration (Day 2-3)
- [ ] Implement MCP client base class
- [ ] Create Gmail tool wrapper
- [ ] Create Search tool wrapper
- [ ] Test MCP tools independently
- [ ] Build MCP HTTP wrappers for Railway

### 🤖 Phase 3: Agent Development (Day 3-5)
- [ ] Implement Planner agent
- [ ] Implement Retriever agent
- [ ] Implement Summarizer agent
- [ ] Implement Verifier agent
- [ ] Implement Email Sender agent
- [ ] Unit test each agent

### 🔀 Phase 4: LangGraph Workflow (Day 5-6)
- [ ] Define ResearchState schema
- [ ] Build LangGraph state machine
- [ ] Implement conditional routing
- [ ] Add checkpointing
- [ ] Integrate LangSmith tracing
- [ ] Test full workflow

### 🎨 Phase 5: Frontend (Day 6-7)
- [ ] Create ResearchForm component
- [ ] Create StatusStream component
- [ ] Create ResultDisplay component
- [ ] Implement SSE connection
- [ ] Add error handling
- [ ] Style with Tailwind + Shadcn/ui

### 🧪 Phase 6: Testing (Day 7-8)
- [ ] Integration tests
- [ ] End-to-end tests
- [ ] Guardrails testing
- [ ] Performance optimization

### 🐳 Phase 7: Dockerization (Day 8-9)
- [ ] Build backend Dockerfile
- [ ] Build MCP server Dockerfiles
- [ ] Test docker-compose locally
- [ ] Implement token storage in PostgreSQL

### 🚀 Phase 8: Railway Deployment (Day 9-10)
- [ ] Create Railway project
- [ ] Deploy backend service
- [ ] Deploy MCP servers
- [ ] Configure PostgreSQL
- [ ] Setup environment variables
- [ ] Test production workflow

---

## 🔑 Required API Keys

| Service | Where to Get | Cost | Required? |
|---------|--------------|------|-----------|
| **Anthropic** | [console.anthropic.com](https://console.anthropic.com/) | ~$0.30/research | ✅ Yes |
| **Brave Search** | [brave.com/search/api](https://brave.com/search/api/) | Free tier: 2000/month | ✅ Yes |
| **LangSmith** | [smith.langchain.com](https://smith.langchain.com/) | Free tier available | ⚠️ Recommended |
| **Google Cloud** | [console.cloud.google.com](https://console.cloud.google.com/) | Free (Gmail API) | ✅ Yes |

---

## 🎓 Learning Path

### Week 1: Foundation & MCP
1. **Day 1-2**: Setup environment, understand MCP protocol
2. **Day 3**: Complete Gmail MCP OAuth flow
3. **Day 4**: Build MCP tool wrappers
4. **Day 5**: Test MCP integration

### Week 2: Agents & Workflow
1. **Day 6-7**: Implement individual agents
2. **Day 8-9**: Build LangGraph workflow
3. **Day 10**: Add guardrails and verification

### Week 3: UI & Deployment
1. **Day 11-12**: Build React UI
2. **Day 13-14**: Docker containerization
3. **Day 15**: Deploy to Railway

---

## 💡 Key Concepts to Understand

### 1. **MCP (Model Context Protocol)**
- Standardized way for LLMs to interact with external tools
- Uses stdio or HTTP transport
- Gmail and Search are MCP servers we connect to

### 2. **LangGraph State Machine**
- Explicit state management with TypedDict
- Nodes = agents (Planner, Retriever, etc.)
- Edges = transitions between agents
- Conditional routing based on verification results

### 3. **Multi-Agent Workflow**
```
User Input → Planner → Retriever → Summarizer → Verifier
                                                    ↓
                                              [Pass/Fail?]
                                                    ↓
                                    Pass → Email Sender → Done
                                    Fail → Summarizer (retry)
```

### 4. **Guardrails**
- **Pydantic**: Structural validation (schema, types)
- **LlamaGuard**: Content safety (harmful content)
- **Custom**: Hallucination detection, citation verification

### 5. **SSE (Server-Sent Events)**
- One-way communication: server → client
- Real-time status updates to UI
- Simpler than WebSockets for this use case

---

## 🚨 Critical Success Factors

### 1. **Gmail MCP Setup** (Highest Risk)
- Most time-consuming step (~45 min first time)
- OAuth flow can be confusing
- **Mitigation**: Follow MCP_INTEGRATION_GUIDE.md step-by-step

### 2. **MCP → LangChain Integration**
- MCP uses stdio, LangChain expects standard tools
- **Solution**: Wrapper classes in `backend/mcp_tools/`

### 3. **Token Storage on Railway**
- Ephemeral filesystem = tokens disappear
- **Solution**: Store in PostgreSQL (encrypted)

### 4. **Cost Management**
- Multiple Claude API calls per research
- **Solution**: Caching, rate limiting, max sub-queries

### 5. **Hallucination Prevention**
- LLMs may fabricate facts
- **Solution**: Strict citations, verification agent, guardrails

---

## 📊 Success Metrics

### Functional
- [ ] User can submit topic + email
- [ ] System generates research plan
- [ ] MCP tools retrieve data
- [ ] Summary includes citations
- [ ] Email sent successfully
- [ ] Real-time status updates work

### Quality
- [ ] Verifier catches hallucinations
- [ ] 90%+ test coverage
- [ ] <2 min end-to-end execution
- [ ] <$0.50 cost per research

### Deployment
- [ ] Docker builds successfully
- [ ] Railway deployment works
- [ ] Workflow recovers from errors

---

## 🆘 When You Need Help

### Documentation
1. Check this index for relevant doc
2. Read the specific guide
3. Check TROUBLESHOOTING.md (when created)

### External Resources
- **MCP Docs**: [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- **LangGraph Docs**: [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/)
- **Anthropic Docs**: [docs.anthropic.com](https://docs.anthropic.com/)
- **Railway Docs**: [docs.railway.app](https://docs.railway.app/)

### Community
- GitHub Issues (for this project)
- LangChain Discord
- Anthropic Discord

---

## 🎯 Next Immediate Steps

1. **Review this index** - Understand project structure
2. **Read PROJECT_CORE.md** - Understand architecture
3. **Follow DEVELOPMENT_SETUP.md** - Get environment running
4. **Complete Gmail MCP setup** - Critical path item
5. **Start Phase 1** - Environment configuration

---

**Project Status**: Foundation Complete ✅  
**Next Phase**: Environment Setup  
**Estimated Time to Working Prototype**: 8-10 days  
**Last Updated**: 2026-03-12
