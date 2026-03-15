# 📚 MCP Research Agent Documentation

Complete documentation for the MCP Research Agent - a production-ready AI-powered research system with multi-agent orchestration using LangGraph, Model Context Protocol, and comprehensive LLM observability via LangSmith.

---

## 📖 **Documentation Structure**

```
docs/
├── README.md                    # This file - documentation index
├── QUICK_START.md              # Get started in 5 minutes
│
├── architecture/               # System architecture & design
│   ├── OVERVIEW.md            # High-level architecture overview
│   ├── ARCHITECTURE.md        # Detailed architecture documentation
│   ├── TECH_STACK.md          # Technology stack details
│   └── PROJECT_CORE.md        # Core concepts and principles
│
├── guides/                     # How-to guides & tutorials
│   ├── WORKFLOW_GUIDE.md      # Complete workflow explanation
│   ├── AGENT_GUIDE.md         # Understanding agents
│   ├── MCP_INTEGRATION_GUIDE.md # MCP integration details
│   └── REDIS_CACHING.md       # Redis caching implementation
│
├── api/                        # API documentation
│   ├── ENDPOINTS.md           # API endpoints reference
│   └── MODELS.md              # Data models and schemas
│
├── setup/                      # Installation & configuration
│   ├── DEVELOPMENT_SETUP.md   # Development environment setup
│   ├── API_KEYS_SETUP.md      # API keys configuration
│   └── TAVILY_SETUP.md        # Tavily search setup
│
├── deployment/                # Production deployment
│   ├── README.md              # Deployment documentation index
│   ├── DEPLOYMENT_GUIDE.md    # Docker & Railway deployment
│   ├── GITHUB_SETUP.md        # Git repository setup
│   └── PRODUCTION_REVIEW.md   # Production readiness checklist
│
├── observability/             # Monitoring & tracing
│   ├── README.md              # Observability documentation index
│   ├── LANGSMITH_IMPLEMENTATION.md # LangSmith setup & usage
│   └── OBSERVABILITY_AUDIT.md # Monitoring recommendations
│
└── troubleshooting/           # Debugging & troubleshooting
    ├── DEBUG_GUIDE.md         # Debugging guide
    └── COMMON_ISSUES.md       # Common issues and solutions
```

---

## 🚀 **Quick Navigation**

### **Getting Started**
- [Quick Start Guide](./QUICK_START.md) - Get up and running in 5 minutes
- [Development Setup](./setup/DEVELOPMENT_SETUP.md) - Complete development environment setup
- [API Keys Setup](./setup/API_KEYS_SETUP.md) - Configure required API keys

### **Understanding the System**
- [Architecture Overview](./architecture/OVERVIEW.md) - High-level system design with diagrams
- [Workflow Guide](./guides/WORKFLOW_GUIDE.md) - Complete workflow explanation with flow diagrams
- [Agent Guide](./guides/AGENT_GUIDE.md) - Understanding each agent's role

### **API Reference**
- [API Endpoints](./api/ENDPOINTS.md) - Complete API documentation
- [Data Models](./api/MODELS.md) - Request/response schemas

### **Advanced Topics**
- [MCP Integration](./guides/MCP_INTEGRATION_GUIDE.md) - Model Context Protocol integration
- [Redis Caching](./guides/REDIS_CACHING.md) - Caching implementation
- [Technology Stack](./architecture/TECH_STACK.md) - Detailed tech stack

### **Deployment & Production**
- [Deployment Guide](./deployment/DEPLOYMENT_GUIDE.md) - Docker & Railway deployment
- [GitHub Setup](./deployment/GITHUB_SETUP.md) - Repository setup and version control
- [Production Review](./deployment/PRODUCTION_REVIEW.md) - Production readiness checklist

### **Observability & Monitoring**
- [LangSmith Implementation](./observability/LANGSMITH_IMPLEMENTATION.md) - Full LLM observability setup
- [Observability Audit](./observability/OBSERVABILITY_AUDIT.md) - Monitoring recommendations
- [Observability Overview](./observability/README.md) - Complete observability guide

### **Troubleshooting**
- [Debug Guide](./troubleshooting/DEBUG_GUIDE.md) - Debugging and logging
- [Common Issues](./troubleshooting/COMMON_ISSUES.md) - Solutions to common problems

---

## 🎯 **What is MCP Research Agent?**

MCP Research Agent is an AI-powered research system that:

✅ **Validates** user queries with intelligent guardrails  
✅ **Plans** research strategy with multiple sub-queries  
✅ **Searches** the web using Tavily AI  
✅ **Synthesizes** findings with Claude Sonnet 4  
✅ **Verifies** accuracy and citations  
✅ **Delivers** results via UI or email  

**Key Features:**
- 🛡️ Input validation guardrails
- 🔄 Multi-agent workflow orchestration
- 📊 Real-time progress tracking
- ✅ Automatic verification
- � **Full LLM observability with LangSmith**
- 💰 **Token usage and cost tracking**
- �💾 Redis caching (optional)
- 📧 Email delivery (optional)
- 📝 Comprehensive logging

---

## 🏗️ **System Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Research Form│  │Progress Track│  │Result Display│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │ SSE Stream
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              LangGraph Workflow                       │   │
│  │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  │   │
│  │  │Valid.│→ │Plan  │→ │Search│→ │Summ. │→ │Verify│  │   │
│  │  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘  │   │
│  │                                      ↓               │   │
│  │                                  ┌──────┐            │   │
│  │                                  │Email │            │   │
│  │                                  └──────┘            │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌────────┐     ┌─────────┐     ┌────────┐
    │Anthropic│     │ Tavily  │     │ Redis  │
    │ Claude  │     │   AI    │     │ Cache  │
    └────────┘     └─────────┘     └────────┘
```

---

## 🔄 **Research Workflow**

```
User Input
    ↓
┌─────────────────┐
│  1. Validation  │ ← Guardrails check
└────────┬────────┘
         ↓ Valid
┌─────────────────┐
│  2. Planning    │ ← Generate sub-queries
└────────┬────────┘
         ↓
┌─────────────────┐
│  3. Retrieval   │ ← Search with Tavily
└────────┬────────┘
         ↓
┌─────────────────┐
│  4. Summarize   │ ← Synthesize with Claude
└────────┬────────┘
         ↓
┌─────────────────┐
│  5. Verify      │ ← Check accuracy
└────────┬────────┘
         ↓
    Pass/Retry (max 1)
         ↓
┌─────────────────┐
│  6. Deliver     │ ← UI or Email
└─────────────────┘
```

---

## 🛠️ **Technology Stack**

**Backend:**
- FastAPI - Web framework
- LangGraph - Workflow orchestration
- LangChain - LLM integration
- Claude Sonnet 4 - AI model
- Tavily AI - Web search
- Redis - Caching (optional)
- SQLite - State persistence

**Frontend:**
- React + TypeScript
- Vite - Build tool
- TailwindCSS - Styling
- Lucide Icons - UI icons

**Infrastructure:**
- Model Context Protocol (MCP)
- Server-Sent Events (SSE)
- LangSmith - Observability

---

## 📦 **Installation**

```bash
# Clone repository
git clone <repo-url>
cd MCPAIResearchAgent

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your API keys

# Start backend
uvicorn api.main:app --reload

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

---

## 🔑 **Required API Keys**

1. **Anthropic API Key** - For Claude Sonnet 4
   - Get it: https://console.anthropic.com/
   
2. **Tavily API Key** - For web search
   - Get it: https://tavily.com/
   
3. **LangSmith API Key** (Optional) - For observability
   - Get it: https://smith.langchain.com/

See [API Keys Setup](./setup/API_KEYS_SETUP.md) for detailed instructions.

---

## 🧪 **Testing**

```bash
# Start backend
cd backend
uvicorn api.main:app --reload

# Start frontend
cd frontend
npm run dev

# Open browser
http://localhost:5173

# Try a research topic
"Latest developments in quantum computing"
```

---

## 📊 **Monitoring & Debugging**

**View logs:**
```bash
cd backend
tail -f logs/research_agent.log
```

**LangSmith tracing:**
- Visit https://smith.langchain.com/
- View traces for your project

See [Debug Guide](./troubleshooting/DEBUG_GUIDE.md) for complete debugging information.

---

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 **License**

MIT License - See LICENSE file for details

---

## 🆘 **Support**

- **Documentation Issues**: Check [Common Issues](./troubleshooting/COMMON_ISSUES.md)
- **Debug Help**: See [Debug Guide](./troubleshooting/DEBUG_GUIDE.md)
- **Questions**: Open an issue on GitHub

---

**Happy Researching! 🚀**
