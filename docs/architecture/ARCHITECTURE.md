# 🏗️ Project Architecture

## 📁 **Directory Structure**

```
MCPAIResearchAgent/
├── backend/                    # Python FastAPI backend
│   ├── .env                   # Backend environment variables (API keys)
│   ├── venv/                  # Python virtual environment
│   ├── config/
│   │   └── settings.py        # Pydantic settings (reads backend/.env)
│   ├── api/
│   │   ├── main.py           # FastAPI app entry point
│   │   └── routes.py         # Research API endpoints
│   ├── agents/               # LangGraph agents
│   │   ├── planner.py        # Research planning agent
│   │   ├── retriever.py      # Web search agent
│   │   ├── summarizer.py     # Summary synthesis agent
│   │   ├── verifier.py       # Fact-checking agent
│   │   └── email_sender.py   # Email delivery agent
│   ├── graph/
│   │   ├── state.py          # LangGraph state schema
│   │   └── workflow.py       # Workflow orchestration
│   ├── mcp_tools/
│   │   ├── mcp_client.py     # Base MCP client
│   │   ├── gmail_tool.py     # Gmail MCP wrapper
│   │   └── search_tool.py    # Tavily search wrapper
│   └── guardrails/
│       └── validators.py     # Input/output validation
│
├── frontend/                  # React + TypeScript frontend
│   ├── .env.local            # Frontend environment variables
│   ├── src/
│   │   ├── App.tsx           # Main application
│   │   ├── components/
│   │   │   ├── ResearchForm.tsx      # Topic/email input form
│   │   │   ├── ProgressTracker.tsx   # Real-time progress display
│   │   │   └── ResultDisplay.tsx     # Summary/citations display
│   │   └── lib/
│   │       └── utils.ts      # Utility functions
│   └── package.json
│
├── mcp_servers/              # MCP server configurations (future)
│   ├── gmail/
│   │   ├── .env             # Gmail MCP credentials
│   │   ├── credentials.json # Google OAuth credentials
│   │   └── token.json       # OAuth access token
│   └── search/
│       └── .env             # Search MCP config
│
├── docs/                     # Documentation
└── .env.example             # Template for all .env files
```

---

## 🔐 **Environment Variable Strategy**

### **Separation of Concerns**

Each service has its own `.env` file for **independent deployment and scaling**:

#### **1. Backend** (`backend/.env`)
```bash
# API Keys
ANTHROPIC_API_KEY=sk-ant-...
TAVILY_API_KEY=tvly-...
LANGSMITH_API_KEY=lsv2_...

# Application Settings
ENVIRONMENT=development
DEBUG=true
MAX_SUB_QUERIES=5
MAX_RETRY_ATTEMPTS=2

# Database
DATABASE_URL=sqlite:///./research_agent.db

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

**Why separate?**
- ✅ Backend can be deployed independently
- ✅ Secrets never exposed to frontend
- ✅ Can scale backend without touching frontend
- ✅ Different environments (dev/staging/prod) per service

#### **2. Frontend** (`frontend/.env.local`)
```bash
# API Configuration
VITE_API_URL=http://localhost:8000
```

**Why separate?**
- ✅ Frontend only knows backend URL
- ✅ No access to API keys or secrets
- ✅ Can point to different backend environments
- ✅ Vite automatically loads `.env.local`

#### **3. MCP Servers** (future: `mcp_servers/*/. env`)
```bash
# Gmail MCP
GMAIL_CREDENTIALS_PATH=./credentials.json
GMAIL_TOKEN_PATH=./token.json

# Search MCP
TAVILY_API_KEY=tvly-...
```

**Why separate?**
- ✅ MCP servers can run as independent microservices
- ✅ Can deploy MCP servers to different infrastructure
- ✅ Easier to add/remove MCP tools
- ✅ Better security isolation

---

## 🚀 **Deployment Scenarios**

### **Scenario 1: Monolith (Current - Development)**
```
Single Machine
├── Backend (port 8000)
├── Frontend (port 5173)
└── Shared .env files
```

**Use case**: Local development, testing

### **Scenario 2: Separated Services (Recommended)**
```
Backend Server
├── backend/.env
└── Backend API (port 8000)

Frontend CDN
├── frontend/.env.local (build time)
└── Static files

MCP Servers (optional)
├── Gmail MCP (port 3001)
└── Search MCP (port 3002)
```

**Use case**: Production, independent scaling

### **Scenario 3: Microservices (Advanced)**
```
Backend Cluster (5 instances)
├── Load Balancer
└── backend/.env (from secrets manager)

Frontend CDN (Vercel/Netlify)
└── VITE_API_URL=https://api.example.com

MCP Gateway
├── Gmail MCP (2 instances)
└── Search MCP (3 instances)
```

**Use case**: High traffic, enterprise

---

## 📊 **Scaling Strategy**

### **Independent Scaling**

Because each service has its own `.env`, you can scale them independently:

#### **Scale Backend Only** (High API usage)
```bash
# Deploy 5 backend instances
docker run -d --env-file backend/.env backend:latest  # Instance 1
docker run -d --env-file backend/.env backend:latest  # Instance 2
docker run -d --env-file backend/.env backend:latest  # Instance 3
docker run -d --env-file backend/.env backend:latest  # Instance 4
docker run -d --env-file backend/.env backend:latest  # Instance 5

# Frontend stays at 1 instance (static files on CDN)
```

#### **Scale Frontend Only** (High traffic)
```bash
# Deploy to CDN (auto-scales)
npm run build
vercel deploy

# Backend stays at 1 instance
```

#### **Scale MCP Servers** (High search volume)
```bash
# Deploy multiple search MCP instances
docker run -d --env-file mcp_servers/search/.env search-mcp:latest  # Instance 1
docker run -d --env-file mcp_servers/search/.env search-mcp:latest  # Instance 2
docker run -d --env-file mcp_servers/search/.env search-mcp:latest  # Instance 3
```

---

## 🔒 **Security Benefits**

### **Principle of Least Privilege**

Each service only has access to what it needs:

| Service | Has Access To | Does NOT Have Access To |
|---------|---------------|-------------------------|
| **Backend** | Anthropic API, Tavily API, Database | Frontend secrets |
| **Frontend** | Backend URL only | API keys, Database |
| **Gmail MCP** | Gmail credentials | Anthropic API, Tavily API |
| **Search MCP** | Tavily API | Gmail credentials, Anthropic API |

### **Secrets Management**

**Development**:
```bash
backend/.env          # Local file
frontend/.env.local   # Local file
```

**Production** (Railway/Vercel):
```bash
# Backend secrets (Railway)
railway variables set ANTHROPIC_API_KEY=sk-ant-...
railway variables set TAVILY_API_KEY=tvly-...

# Frontend env (Vercel)
vercel env add VITE_API_URL production
```

---

## 🧪 **Testing Strategy**

### **Unit Tests** (per service)
```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
```

### **Integration Tests** (cross-service)
```bash
# Test backend + MCP
cd backend
pytest tests/integration/

# Test frontend + backend
cd frontend
npm run test:e2e
```

### **End-to-End Tests** (full workflow)
```bash
# Playwright/Cypress tests
npm run test:e2e:full
```

---

## 📦 **Deployment Checklist**

### **Backend Deployment**
- [ ] Set `backend/.env` variables in production
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=false`
- [ ] Configure production database URL
- [ ] Set up CORS for production frontend URL
- [ ] Enable HTTPS
- [ ] Set up health check endpoint monitoring

### **Frontend Deployment**
- [ ] Set `VITE_API_URL` to production backend
- [ ] Build with `npm run build`
- [ ] Deploy to CDN (Vercel/Netlify)
- [ ] Configure custom domain
- [ ] Enable HTTPS
- [ ] Set up error tracking (Sentry)

### **MCP Servers Deployment** (optional)
- [ ] Set up Gmail OAuth in production
- [ ] Configure MCP server URLs in backend
- [ ] Deploy MCP servers as separate services
- [ ] Set up health checks
- [ ] Configure rate limiting

---

## 🎯 **Summary**

### **Current Architecture** ✅
- **Separated `.env` files** for backend and frontend
- **Independent deployment** capability
- **Better security** (secrets isolation)
- **Scalable** (can scale services independently)

### **Why This is Better** 🚀
1. **Production-ready** - Follows industry best practices
2. **Secure** - Principle of least privilege
3. **Scalable** - Independent service scaling
4. **Maintainable** - Clear separation of concerns
5. **Flexible** - Easy to add/remove services

---

**This architecture supports both monolith (development) and microservices (production) deployment models!** 🎉
