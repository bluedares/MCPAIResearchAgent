# 🏗️ Architecture Overview

High-level architecture of the MCP Research Agent system.

---

## 📐 **System Architecture Diagram**

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                               │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    Frontend (React + Vite)                    │  │
│  │                                                                │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │  │
│  │  │              │  │              │  │              │       │  │
│  │  │  Research    │  │  Progress    │  │   Result     │       │  │
│  │  │    Form      │  │   Tracker    │  │   Display    │       │  │
│  │  │              │  │              │  │              │       │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘       │  │
│  │                                                                │  │
│  └────────────────────────────┬───────────────────────────────────┘  │
└───────────────────────────────┼──────────────────────────────────────┘
                                │
                                │ HTTP/SSE
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                         BACKEND API                                   │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    FastAPI Server                             │  │
│  │                                                                │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │  │
│  │  │   Config     │  │  Research    │  │  Send Email  │       │  │
│  │  │  Endpoint    │  │   Stream     │  │  Endpoint    │       │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘       │  │
│  │                                                                │  │
│  └────────────────────────────┬───────────────────────────────────┘  │
│                                │                                      │
│  ┌────────────────────────────▼───────────────────────────────────┐  │
│  │                    LangGraph Workflow Engine                   │  │
│  │                                                                 │  │
│  │  ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐       │  │
│  │  │Topic │ → │Plan  │ → │Retri │ → │Summ  │ → │Verify│       │  │
│  │  │Valid.│   │ner   │   │ever  │   │arizer│   │      │       │  │
│  │  └──────┘   └──────┘   └──────┘   └──────┘   └──┬───┘       │  │
│  │                                                   │            │  │
│  │                                                   ↓            │  │
│  │                                              ┌──────┐          │  │
│  │                                              │Email │          │  │
│  │                                              │Sender│          │  │
│  │                                              └──────┘          │  │
│  │                                                                 │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    Support Services                           │  │
│  │                                                                │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │  │
│  │  │   Logging    │  │    Redis     │  │   SQLite     │       │  │
│  │  │   System     │  │    Cache     │  │   Storage    │       │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘       │  │
│  │                                                                │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │  Anthropic   │ │   Tavily     │ │  LangSmith   │
        │   Claude     │ │     AI       │ │  Tracing     │
        │  Sonnet 4    │ │   Search     │ │  (Optional)  │
        └──────────────┘ └──────────────┘ └──────────────┘
```

---

## 🔄 **Data Flow**

### **1. Request Flow**

```
User Input
    │
    ├─→ Frontend validates input (client-side)
    │
    ├─→ HTTP POST to /api/research/{id}/stream
    │
    ├─→ Backend validates topic (Topic Validator Agent)
    │       │
    │       ├─ Invalid → Return error with suggestion
    │       └─ Valid → Continue
    │
    ├─→ Check Redis cache (if enabled)
    │       │
    │       ├─ Cache HIT → Return cached result
    │       └─ Cache MISS → Continue
    │
    ├─→ Initialize LangGraph workflow
    │
    └─→ Stream SSE events to frontend
```

### **2. Workflow Execution**

```
┌─────────────────────────────────────────────────────────────┐
│                    LangGraph State Machine                   │
└─────────────────────────────────────────────────────────────┘

State: ResearchState
├─ topic: str
├─ research_plan: dict
├─ sub_queries: list
├─ raw_data: list
├─ sources: list
├─ summary: str
├─ citations: list
├─ verification_status: str
├─ verified: bool
└─ current_step: str

Flow:
┌──────────────┐
│ Topic        │ ← Validates input
│ Validator    │   Rejects: personal, vague, inappropriate
└──────┬───────┘
       │ Valid
       ▼
┌──────────────┐
│ Planner      │ ← Generates 3-5 sub-queries
│ Agent        │   Uses Claude to create research strategy
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Retriever    │ ← Searches web with Tavily
│ Agent        │   Executes each sub-query
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Summarizer   │ ← Synthesizes findings with Claude
│ Agent        │   Creates structured summary + citations
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Verifier     │ ← Checks accuracy and citations
│ Agent        │   Confidence scoring
└──────┬───────┘
       │
       ├─ Pass → Email Sender
       │
       └─ Fail → Retry (max 1) → Force Pass
              │
              ▼
       ┌──────────────┐
       │ Email Sender │ ← Sends results (if email provided)
       │ Agent        │   Or displays in UI
       └──────────────┘
```

---

## 🧩 **Component Architecture**

### **Frontend Components**

```
src/
├── App.tsx                    # Main application component
│   ├── State management
│   ├── SSE event handling
│   └── Component orchestration
│
├── components/
│   ├── ResearchForm.tsx      # Input form
│   │   ├── Topic validation
│   │   ├── Email input (conditional)
│   │   └── Submit handling
│   │
│   ├── ProgressTracker.tsx   # Real-time progress
│   │   ├── Step indicators
│   │   ├── Status messages
│   │   └── Loading states
│   │
│   └── ResultDisplay.tsx     # Results presentation
│       ├── Summary display
│       ├── Citations list
│       ├── Verification badge
│       └── Email sender (conditional)
│
└── types/
    └── Citation interface
```

### **Backend Components**

```
backend/
├── api/
│   ├── main.py               # FastAPI application
│   │   ├── CORS configuration
│   │   ├── Lifespan events
│   │   └── Route registration
│   │
│   └── routes.py             # API endpoints
│       ├── GET /api/config
│       ├── GET /api/research/{id}/stream
│       └── POST /api/send-email
│
├── agents/
│   ├── topic_validator.py    # Input validation
│   ├── planner.py            # Research planning
│   ├── retriever.py          # Web search
│   ├── summarizer.py         # Content synthesis
│   ├── verifier.py           # Quality verification
│   └── email_sender.py       # Email delivery
│
├── graph/
│   ├── state.py              # State definition
│   └── workflow.py           # Workflow orchestration
│
├── mcp_tools/
│   ├── search_tool.py        # Tavily integration
│   └── gmail_tool.py         # Gmail integration
│
├── utils/
│   ├── logger.py             # Logging system
│   └── redis_cache.py        # Caching layer
│
└── config/
    └── settings.py           # Configuration management
```

---

## 🔐 **Security Architecture**

### **Input Validation**

```
User Input
    ↓
┌─────────────────────────────┐
│  Frontend Validation        │
│  - Length check (10-500)    │
│  - Email format validation  │
└────────────┬────────────────┘
             ↓
┌─────────────────────────────┐
│  Backend Validation         │
│  - Topic Validator Agent    │
│  - Claude-based analysis    │
│  - Guardrails enforcement   │
└─────────────────────────────┘
```

### **API Security**

- **CORS**: Configured for localhost development
- **Rate Limiting**: Can be added via middleware
- **API Keys**: Stored in environment variables
- **Input Sanitization**: Pydantic models validate all inputs

### **Data Privacy**

- **No PII Storage**: Personal questions rejected
- **Session Isolation**: Each workflow has unique ID
- **Cache Keys**: Hashed topic identifiers
- **Logs**: No sensitive data logged

---

## 📊 **State Management**

### **Backend State (LangGraph)**

```python
class ResearchState(TypedDict):
    # Input
    topic: str
    client_email: str
    
    # Planning
    research_plan: Optional[Dict]
    sub_queries: List[str]
    
    # Retrieval
    raw_data: List[Dict]
    sources: List[str]
    
    # Summarization
    summary: str
    citations: List[Dict]
    
    # Verification
    verification_status: str
    verification_confidence: float
    verified: bool
    
    # Metadata
    workflow_id: str
    current_step: str
    retry_count: int
    status_messages: List[str]
```

### **Frontend State (React)**

```typescript
// App.tsx state
const [isResearching, setIsResearching] = useState(false)
const [currentStep, setCurrentStep] = useState('')
const [messages, setMessages] = useState<string[]>([])
const [summary, setSummary] = useState('')
const [citations, setCitations] = useState<Citation[]>([])
const [verified, setVerified] = useState(true)
const [emailEnabled, setEmailEnabled] = useState(false)
const [error, setError] = useState('')
```

---

## 🔄 **Communication Patterns**

### **Server-Sent Events (SSE)**

```
Frontend                          Backend
   │                                 │
   ├─ Open EventSource ─────────────>│
   │                                 │
   │<─────── start event ────────────┤
   │                                 │
   │<─────── update events ──────────┤ (multiple)
   │         (step, messages)        │
   │                                 │
   │<─────── complete event ─────────┤
   │         (summary, citations)    │
   │                                 │
   ├─ Close EventSource              │
```

### **Event Types**

```typescript
// SSE Event Types
type SSEEvent = 
  | { type: 'start', workflow_id: string }
  | { type: 'update', step: string, messages: string[] }
  | { type: 'complete', summary: string, citations: Citation[] }
  | { type: 'validation_error', error: string, suggestion: string }
  | { type: 'error', error: string }
```

---

## 💾 **Data Persistence**

### **SQLite (LangGraph State)**

```
data/research_agent.db
├── checkpoints          # Workflow state snapshots
├── checkpoint_writes    # State updates
└── checkpoint_blobs     # Binary data
```

### **Redis (Optional Caching)**

```
Redis Keys:
├── research:{topic_hash}              # Cached results
├── research:{topic_hash}:{email_hash} # Personalized results
└── TTL: 24 hours
```

### **File System (Logs)**

```
logs/
├── research_agent.log   # All application logs
├── agents.log           # Agent-specific logs
└── workflow.log         # Workflow routing logs
```

---

## 🔌 **External Integrations**

### **Anthropic Claude**

```
Purpose: AI reasoning and generation
Model: claude-sonnet-4-20250514
Usage:
  - Topic validation
  - Research planning
  - Content summarization
  - Quality verification
```

### **Tavily AI**

```
Purpose: Web search
API: Tavily Search API
Usage:
  - Execute sub-queries
  - Retrieve web content
  - Extract relevant information
```

### **LangSmith (Optional)**

```
Purpose: Observability and tracing
Usage:
  - Trace LLM calls
  - Monitor performance
  - Debug workflows
  - Track costs
```

---

## 🎯 **Design Principles**

1. **Modularity**: Each agent is independent and reusable
2. **Fail-Safe**: Graceful degradation on errors
3. **Observable**: Comprehensive logging and tracing
4. **Scalable**: Stateless design with optional caching
5. **User-Centric**: Clear feedback and error messages
6. **Cost-Effective**: Validation before expensive operations

---

## 📈 **Performance Characteristics**

| Operation | Time | Cost |
|-----------|------|------|
| Topic Validation | 0.5-1s | $0.001 |
| Planning | 2-5s | $0.02 |
| Retrieval | 5-10s | $0.05 |
| Summarization | 15-30s | $0.12 |
| Verification | 5-10s | $0.03 |
| **Total** | **30-60s** | **$0.20-0.30** |

**With Caching:**
- Cache HIT: < 100ms, $0.00
- Hit Rate: 40-60% in production

---

## 🔮 **Future Enhancements**

- [ ] Multi-language support
- [ ] PDF export
- [ ] Custom research templates
- [ ] Collaborative research
- [ ] Advanced analytics
- [ ] Mobile app

---

**Next:** [Workflow Guide](../guides/WORKFLOW_GUIDE.md) for detailed workflow explanation.
