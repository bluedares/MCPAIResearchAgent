# TECH STACK - Complete Technology Reference

**Comprehensive guide to all technologies, packages, and versions used in the MCP Research Agent**

---

## 🐍 Backend Stack (Python 3.12)

### Core Framework & API

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **FastAPI** | 0.115.0 | Modern async web framework | [docs](https://fastapi.tiangolo.com/) |
| **Uvicorn** | 0.30.6 | ASGI server with WebSocket support | [docs](https://www.uvicorn.org/) |
| **python-dotenv** | 1.0.1 | Environment variable management | [docs](https://pypi.org/project/python-dotenv/) |
| **sse-starlette** | 2.1.3 | Server-Sent Events for FastAPI | [docs](https://github.com/sysid/sse-starlette) |

### LangChain Ecosystem

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **langchain** | 0.3.1 | LLM application framework | [docs](https://python.langchain.com/) |
| **langchain-anthropic** | 0.2.1 | Anthropic integration | [docs](https://python.langchain.com/docs/integrations/platforms/anthropic) |
| **langchain-community** | 0.3.1 | Community integrations | [docs](https://python.langchain.com/docs/integrations/platforms/) |
| **langgraph** | 0.2.28 | Multi-agent workflow orchestration | [docs](https://langchain-ai.github.io/langgraph/) |
| **langsmith** | 0.1.129 | Tracing and evaluation platform | [docs](https://docs.smith.langchain.com/) |

**Why LangGraph?**
- ✅ Explicit state management with TypedDict
- ✅ Built-in checkpointing for long workflows
- ✅ Conditional routing (verification pass/fail)
- ✅ Better observability than LCEL chains

### LLM Provider

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **anthropic** | 0.39.0 | Claude API client | [docs](https://docs.anthropic.com/claude/reference/client-sdks) |

**Model Used**: `claude-sonnet-4-20250514`
- Context window: 200K tokens
- Best for: Reasoning, citations, factual accuracy
- Cost: ~$3 per 1M input tokens, ~$15 per 1M output tokens

### MCP (Model Context Protocol)

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **mcp** | 1.0.0 | MCP client for Python | [docs](https://modelcontextprotocol.io/) |

**MCP Servers Used** (Node.js):
- `@modelcontextprotocol/server-gmail` - Gmail integration
- `@modelcontextprotocol/server-brave-search` - Web search

### Validation & Type Safety

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **pydantic** | 2.9.2 | Data validation and settings | [docs](https://docs.pydantic.dev/) |
| **pydantic-settings** | 2.5.2 | Settings management | [docs](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) |

**Use Cases**:
- ResearchState schema validation
- API request/response models
- Environment variable validation
- Agent input/output schemas

### Database & Persistence

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **sqlalchemy** | 2.0.35 | SQL toolkit and ORM | [docs](https://docs.sqlalchemy.org/) |
| **alembic** | 1.13.3 | Database migrations | [docs](https://alembic.sqlalchemy.org/) |
| **psycopg2-binary** | 2.9.9 | PostgreSQL adapter | [docs](https://www.psycopg.org/) |
| **aiosqlite** | 0.20.0 | Async SQLite driver | [docs](https://aiosqlite.omnilib.dev/) |

**Database Strategy**:
- **Local**: SQLite for LangGraph checkpoints
- **Production**: PostgreSQL on Railway for state + OAuth tokens

### Caching (Optional)

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **redis** | 5.1.1 | Redis client | [docs](https://redis-py.readthedocs.io/) |
| **hiredis** | 3.0.0 | High-performance Redis parser | [docs](https://github.com/redis/hiredis-py) |

**Use Cases**:
- Cache search results (avoid duplicate API calls)
- Rate limiting
- Session management

### Guardrails & Safety

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **llama-guard** | 0.1.0 | Content safety filtering | [docs](https://github.com/meta-llama/llama-guard) |
| **cryptography** | 43.0.1 | Token encryption | [docs](https://cryptography.io/) |

**Note**: LlamaGuard package may need alternative. Consider:
- NeMo Guardrails
- Custom hallucination detection
- Anthropic's built-in safety features

### HTTP & Async

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **httpx** | 0.27.2 | Async HTTP client | [docs](https://www.python-httpx.org/) |
| **aiohttp** | 3.10.8 | Async HTTP server/client | [docs](https://docs.aiohttp.org/) |
| **tenacity** | 9.0.0 | Retry logic with backoff | [docs](https://tenacity.readthedocs.io/) |

### Utilities

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **python-multipart** | 0.0.12 | Form data parsing | [docs](https://github.com/andrew-d/python-multipart) |
| **email-validator** | 2.2.0 | Email validation | [docs](https://github.com/JoshData/python-email-validator) |

### Testing

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **pytest** | 8.3.3 | Testing framework | [docs](https://docs.pytest.org/) |
| **pytest-asyncio** | 0.24.0 | Async test support | [docs](https://pytest-asyncio.readthedocs.io/) |
| **pytest-cov** | 5.0.0 | Coverage reporting | [docs](https://pytest-cov.readthedocs.io/) |
| **pytest-mock** | 3.14.0 | Mocking utilities | [docs](https://pytest-mock.readthedocs.io/) |

### Development Tools

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **black** | 24.8.0 | Code formatter | [docs](https://black.readthedocs.io/) |
| **ruff** | 0.6.9 | Fast Python linter | [docs](https://docs.astral.sh/ruff/) |
| **mypy** | 1.11.2 | Static type checker | [docs](https://mypy.readthedocs.io/) |
| **pre-commit** | 3.8.0 | Git hooks framework | [docs](https://pre-commit.com/) |

---

## ⚛️ Frontend Stack (React + TypeScript)

### Core Framework

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **react** | 18.3.1 | UI library | [docs](https://react.dev/) |
| **react-dom** | 18.3.1 | React DOM renderer | [docs](https://react.dev/reference/react-dom) |
| **typescript** | 5.6.2 | Type-safe JavaScript | [docs](https://www.typescriptlang.org/) |
| **vite** | 5.4.8 | Fast build tool | [docs](https://vitejs.dev/) |

**Why Vite?**
- ⚡ Lightning-fast HMR (Hot Module Replacement)
- 📦 Optimized production builds
- 🔧 Zero-config TypeScript support
- 🎯 Better than Create React App

### UI Components & Styling

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **shadcn/ui** | Latest | Accessible component library | [docs](https://ui.shadcn.com/) |
| **tailwindcss** | 3.4.13 | Utility-first CSS | [docs](https://tailwindcss.com/) |
| **lucide-react** | 0.446.0 | Icon library | [docs](https://lucide.dev/) |
| **class-variance-authority** | 0.7.0 | Component variants | [docs](https://cva.style/docs) |
| **clsx** | 2.1.1 | Conditional classes | [docs](https://github.com/lukeed/clsx) |
| **tailwind-merge** | 2.5.2 | Merge Tailwind classes | [docs](https://github.com/dcastil/tailwind-merge) |

**Shadcn/ui Components Used**:
- `Input` - Email input
- `Textarea` - Topic input
- `Button` - Submit button
- `Card` - Layout containers
- `Progress` - Status indicator
- `Alert` - Error messages
- `Badge` - Status badges

### State Management

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **@tanstack/react-query** | 5.56.2 | Server state management | [docs](https://tanstack.com/query/latest) |

**Why React Query?**
- ✅ Automatic caching and refetching
- ✅ SSE/EventSource integration
- ✅ Loading/error states built-in
- ✅ No Redux boilerplate

### Forms & Validation

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **react-hook-form** | 7.53.0 | Form state management | [docs](https://react-hook-form.com/) |
| **zod** | 3.23.8 | Schema validation | [docs](https://zod.dev/) |
| **@hookform/resolvers** | 3.9.0 | Zod + React Hook Form | [docs](https://github.com/react-hook-form/resolvers) |

**Form Schema Example**:
```typescript
const researchSchema = z.object({
  topic: z.string().min(10).max(500),
  clientEmail: z.string().email()
});
```

### Build & Development

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **@vitejs/plugin-react** | 4.3.1 | React plugin for Vite | [docs](https://github.com/vitejs/vite-plugin-react) |
| **autoprefixer** | 10.4.20 | CSS vendor prefixes | [docs](https://autoprefixer.github.io/) |
| **postcss** | 8.4.47 | CSS transformations | [docs](https://postcss.org/) |

### TypeScript & Linting

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **@typescript-eslint/eslint-plugin** | 8.7.0 | TypeScript linting | [docs](https://typescript-eslint.io/) |
| **@typescript-eslint/parser** | 8.7.0 | TypeScript parser | [docs](https://typescript-eslint.io/) |
| **eslint** | 9.11.1 | JavaScript linter | [docs](https://eslint.org/) |
| **eslint-plugin-react-hooks** | 4.6.2 | React Hooks rules | [docs](https://www.npmjs.com/package/eslint-plugin-react-hooks) |
| **eslint-plugin-react-refresh** | 0.4.12 | React Refresh rules | [docs](https://github.com/ArnaudBarre/eslint-plugin-react-refresh) |

---

## 🐳 DevOps & Deployment

### Containerization

| Technology | Version | Purpose | Documentation |
|------------|---------|---------|---------------|
| **Docker** | 24+ | Container runtime | [docs](https://docs.docker.com/) |
| **Docker Compose** | 2.20+ | Multi-container orchestration | [docs](https://docs.docker.com/compose/) |

**Containers**:
1. Backend (Python + FastAPI)
2. Gmail MCP Server (Node.js)
3. Search MCP Server (Node.js)
4. PostgreSQL (state storage)
5. Redis (optional caching)

### Cloud Platform

| Technology | Purpose | Documentation |
|------------|---------|---------------|
| **Railway** | PaaS deployment | [docs](https://docs.railway.app/) |

**Railway Features Used**:
- Multi-service deployment
- PostgreSQL database
- Redis (optional)
- Environment variables
- GitHub auto-deploy
- Custom domains

**Alternatives Considered**:
- ❌ Heroku (expensive)
- ❌ AWS ECS (complex setup)
- ❌ Render (limited free tier)
- ✅ Railway (best balance)

### CI/CD

| Technology | Purpose | Documentation |
|------------|---------|---------------|
| **GitHub Actions** | Automated testing & deployment | [docs](https://docs.github.com/en/actions) |

**Workflows**:
- Run tests on PR
- Build Docker images
- Deploy to Railway on merge to main

---

## 🔧 MCP Servers (Node.js)

### Gmail MCP

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **@modelcontextprotocol/server-gmail** | Latest | Gmail API integration | [docs](https://github.com/modelcontextprotocol/servers) |
| **express** | 4.18+ | HTTP wrapper for Railway | [docs](https://expressjs.com/) |
| **uuid** | 9.0+ | Request ID generation | [docs](https://github.com/uuidjs/uuid) |

**Tools Provided**:
- `send_email(to, subject, body)`
- `search_emails(query)` (optional)
- `get_email(id)` (optional)

### Search MCP

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **@modelcontextprotocol/server-brave-search** | Latest | Brave Search API | [docs](https://github.com/modelcontextprotocol/servers) |
| **express** | 4.18+ | HTTP wrapper | [docs](https://expressjs.com/) |

**Tools Provided**:
- `web_search(query, count)`

---

## 📊 Observability & Monitoring

### LangSmith

| Feature | Purpose | Documentation |
|---------|---------|---------------|
| **Traces** | Workflow execution tracking | [docs](https://docs.smith.langchain.com/) |
| **Evaluators** | Citation accuracy verification | [docs](https://docs.smith.langchain.com/evaluation) |
| **Metrics** | Latency, cost, success rate | [docs](https://docs.smith.langchain.com/observability) |
| **Datasets** | Test case management | [docs](https://docs.smith.langchain.com/datasets) |

**Metrics Tracked**:
- Workflow duration
- Token usage per agent
- API costs
- Success/failure rates
- Verification pass rates

### Railway Logs

- Structured JSON logs
- Real-time log streaming
- Log retention (7 days free tier)

---

## 🔐 Security & Secrets

### Environment Variables

| Variable | Purpose | Storage |
|----------|---------|---------|
| `ANTHROPIC_API_KEY` | Claude API access | Railway Secrets |
| `BRAVE_API_KEY` | Search API access | Railway Secrets |
| `LANGSMITH_API_KEY` | Observability | Railway Secrets |
| `GMAIL_REFRESH_TOKEN` | OAuth token | PostgreSQL (encrypted) |
| `DATABASE_URL` | PostgreSQL connection | Auto-injected by Railway |

### Encryption

- **cryptography** package for token encryption
- AES-256 encryption for OAuth tokens
- Fernet symmetric encryption

---

## 💰 Cost Breakdown

### API Costs (per 100 researches)

| Service | Cost | Notes |
|---------|------|-------|
| Claude API | ~$30 | 3 calls per research (Planner, Summarizer, Verifier) |
| Brave Search | ~$5 | 5 queries per research |
| Gmail API | Free | 250 emails/day limit |
| **Total API** | **~$35** | |

### Infrastructure Costs (monthly)

| Service | Cost | Notes |
|---------|------|-------|
| Railway | $5 | Free tier credit |
| PostgreSQL | Included | Railway managed |
| Redis | Included | Railway managed (optional) |
| **Total Infra** | **$5** | |

**Grand Total**: ~$40/month for 100 researches

---

## 🎯 Version Compatibility Matrix

| Python | Node.js | Docker | Railway |
|--------|---------|--------|---------|
| 3.12+ | 18+ | 24+ | Latest |

**Tested Combinations**:
- ✅ Python 3.12 + Node 18 + Docker 24
- ✅ Python 3.12 + Node 20 + Docker 25
- ❌ Python 3.11 (not tested)

---

## 📦 Installation Commands

### Backend
```bash
pip install -r requirements.txt
```

### Frontend
```bash
npm install
```

### MCP Servers
```bash
npx -y @modelcontextprotocol/server-gmail
npx -y @modelcontextprotocol/server-brave-search
```

---

## 🔄 Update Strategy

### Dependency Updates
```bash
# Backend
pip list --outdated
pip install --upgrade <package>

# Frontend
npm outdated
npm update <package>
```

### Security Audits
```bash
# Python
pip-audit

# Node.js
npm audit
npm audit fix
```

---

**Last Updated**: 2026-03-12  
**Maintained By**: Development Team
