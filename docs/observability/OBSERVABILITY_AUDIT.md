# Observability & Monitoring Audit

## Current Implementation Review

### ✅ What's Already Implemented

#### 1. **Basic Logging System**
**Location**: `backend/utils/logger.py`

**Current Features**:
- ✅ File-based logging (3 separate log files)
  - `logs/research_agent.log` - General application logs
  - `logs/agents.log` - Agent-specific logs
  - `logs/workflow.log` - Workflow execution logs
- ✅ Console logging with simple format
- ✅ Detailed file logging with timestamps
- ✅ Agent-specific loggers (planner, retriever, summarizer, verifier, email_sender)
- ✅ Workflow logger
- ✅ Suppression of noisy libraries (httpx, httpcore, urllib3)

**What's Logged**:
- Application startup
- Environment configuration
- Agent execution steps
- Workflow state transitions

#### 2. **LangSmith Configuration**
**Location**: `backend/config/settings.py`

**Current Setup**:
```python
langsmith_api_key: Optional[str] = None
langsmith_project: str = "mcp-research-agent"
langsmith_tracing_v2: bool = True
```

**Status**: ⚠️ **Configured but NOT actively used in code**

#### 3. **Status Messages**
**Location**: `backend/graph/workflow.py`

**Current Implementation**:
- ✅ Status messages added to state at each node
- ✅ Messages track workflow progress
- ✅ Streamed to frontend via SSE

**Example**:
```python
state["status_messages"].append("🧠 Planning research strategy...")
state["status_messages"].append(f"✅ Generated {len(plan['sub_queries'])} sub-queries")
```

---

## ❌ What's Missing (Critical Gaps)

### 1. **LangSmith Tracing** - NOT IMPLEMENTED
**Impact**: No visibility into LLM calls, prompts, or token usage

**What's Missing**:
- ❌ No `@traceable` decorators on agent functions
- ❌ No LangSmith callbacks in LLM chains
- ❌ No automatic tracing of LangGraph workflow
- ❌ No token usage tracking
- ❌ No cost calculation per request

### 2. **Request Logging** - MINIMAL
**Impact**: Can't track individual requests or debug issues

**What's Missing**:
- ❌ No request ID generation/tracking
- ❌ No structured logging (JSON format)
- ❌ No request metadata (user, timestamp, duration)
- ❌ No correlation between logs and requests

### 3. **Prompt Logging** - NOT IMPLEMENTED
**Impact**: Can't debug prompt issues or optimize prompts

**What's Missing**:
- ❌ No prompt templates logged
- ❌ No actual prompts sent to LLM logged
- ❌ No LLM responses logged
- ❌ No prompt versioning

### 4. **Tool Execution Logs** - MINIMAL
**Impact**: Can't see what MCP tools are doing

**What's Missing**:
- ❌ No MCP tool call logging
- ❌ No tool input/output logging
- ❌ No tool execution time tracking
- ❌ No tool error logging

### 5. **Latency Tracking** - NOT IMPLEMENTED
**Impact**: Can't identify performance bottlenecks

**What's Missing**:
- ❌ No per-agent timing
- ❌ No per-LLM-call timing
- ❌ No per-tool-call timing
- ❌ No total request duration
- ❌ No P95/P99 metrics

### 6. **Token Usage Metrics** - NOT IMPLEMENTED
**Impact**: Can't track costs or optimize token usage

**What's Missing**:
- ❌ No input token counting
- ❌ No output token counting
- ❌ No token usage per agent
- ❌ No cumulative token tracking
- ❌ No token usage trends

### 7. **Cost Monitoring** - NOT IMPLEMENTED
**Impact**: No visibility into spending

**What's Missing**:
- ❌ No cost calculation per request
- ❌ No cost breakdown by agent
- ❌ No cost tracking over time
- ❌ No cost alerts
- ❌ No budget monitoring

---

## 🚀 Quick Wins (Minimal Code Changes)

### Priority 1: Enable LangSmith Tracing (5 minutes)

**Why**: Instant visibility into all LLM calls, prompts, tokens, and costs

**Implementation**:

#### Step 1: Add Environment Variables
Already configured in `settings.py`, just need to set in `.env`:
```bash
LANGSMITH_API_KEY=lsv2_pt_your_key_here
LANGSMITH_PROJECT=mcp-research-agent
LANGSMITH_TRACING_V2=true
```

#### Step 2: Enable Tracing in Agent Functions
Add `@traceable` decorator to agent functions:

```python
# backend/agents/planner.py
from langsmith import traceable

@traceable(name="planner_agent", run_type="llm")
async def plan_research(topic: str) -> Dict[str, Any]:
    # Existing code - NO CHANGES NEEDED
    # LangSmith will automatically track:
    # - Input: topic
    # - Output: research plan
    # - LLM calls: Claude API calls
    # - Tokens: input/output tokens
    # - Cost: calculated automatically
    # - Latency: execution time
    ...
```

**Apply to all agents**:
- `agents/planner.py` - `plan_research()`
- `agents/retriever.py` - `retrieve_information()`
- `agents/summarizer.py` - `summarize_research()`
- `agents/verifier.py` - `verify_research()`
- `agents/email_sender.py` - `send_research_email()`

#### Step 3: Enable Workflow Tracing
```python
# backend/graph/workflow.py
from langsmith import traceable

@traceable(name="research_workflow", run_type="chain")
async def run_research_workflow(topic: str, client_email: str) -> Dict[str, Any]:
    # Existing code - NO CHANGES NEEDED
    ...
```

**Result**: 
- ✅ Full trace visualization in LangSmith
- ✅ Automatic token counting
- ✅ Automatic cost calculation
- ✅ Latency tracking per agent
- ✅ Prompt/response logging

**Effort**: 5 minutes (add decorators)  
**Impact**: 🔥 MASSIVE - Full observability instantly

---

### Priority 2: Add Request ID Tracking (10 minutes)

**Why**: Correlate logs across distributed systems

**Implementation**:

```python
# backend/api/middleware/request_id.py (NEW FILE)
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
```

```python
# backend/api/main.py
from api.middleware.request_id import RequestIDMiddleware

app.add_middleware(RequestIDMiddleware)
```

```python
# backend/utils/logger.py - UPDATE
class RequestContextFilter(logging.Filter):
    def filter(self, record):
        # Add request_id to all log records
        from contextvars import ContextVar
        request_id_var: ContextVar[str] = ContextVar('request_id', default='no-request-id')
        record.request_id = request_id_var.get()
        return True

# Update formatter
detailed_formatter = logging.Formatter(
    '%(asctime)s | %(request_id)s | %(levelname)-8s | %(name)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
```

**Result**:
- ✅ Every log has request ID
- ✅ Can trace request across services
- ✅ Easy debugging

**Effort**: 10 minutes  
**Impact**: 🔥 HIGH - Much easier debugging

---

### Priority 3: Add Structured Logging (15 minutes)

**Why**: Machine-readable logs for analysis

**Implementation**:

```python
# backend/utils/structured_logger.py (NEW FILE)
import json
import logging
from datetime import datetime
from typing import Any, Dict

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def log_event(self, event_type: str, data: Dict[str, Any], level: str = "INFO"):
        """Log structured event."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "level": level,
            **data
        }
        
        log_method = getattr(self.logger, level.lower())
        log_method(json.dumps(log_entry))
    
    def log_llm_call(self, agent: str, model: str, input_tokens: int, 
                     output_tokens: int, latency_ms: float, cost: float):
        """Log LLM call metrics."""
        self.log_event("llm_call", {
            "agent": agent,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "latency_ms": latency_ms,
            "cost_usd": cost
        })
    
    def log_tool_call(self, tool: str, input_data: Any, output_data: Any, 
                      latency_ms: float, success: bool):
        """Log tool execution."""
        self.log_event("tool_call", {
            "tool": tool,
            "input": str(input_data)[:200],  # Truncate
            "output": str(output_data)[:200],
            "latency_ms": latency_ms,
            "success": success
        })
    
    def log_request(self, request_id: str, topic: str, email: str, 
                    total_duration_ms: float, total_cost: float, success: bool):
        """Log complete request."""
        self.log_event("research_request", {
            "request_id": request_id,
            "topic": topic,
            "email": email,
            "total_duration_ms": total_duration_ms,
            "total_cost_usd": total_cost,
            "success": success
        })
```

**Usage in agents**:
```python
# backend/agents/planner.py
from utils.structured_logger import StructuredLogger
import time

logger = StructuredLogger(__name__)

async def plan_research(topic: str) -> Dict[str, Any]:
    start_time = time.time()
    
    # Existing code...
    result = await chain.ainvoke({"topic": topic})
    
    latency_ms = (time.time() - start_time) * 1000
    
    # Log structured event
    logger.log_llm_call(
        agent="planner",
        model="claude-sonnet-4",
        input_tokens=len(topic.split()) * 1.3,  # Rough estimate
        output_tokens=len(str(result)) // 4,     # Rough estimate
        latency_ms=latency_ms,
        cost=0.015  # Estimate
    )
    
    return result
```

**Result**:
- ✅ JSON logs for easy parsing
- ✅ Metrics in logs
- ✅ Can build dashboards from logs

**Effort**: 15 minutes  
**Impact**: 🔥 HIGH - Enables analytics

---

### Priority 4: Add Simple Metrics Tracking (20 minutes)

**Why**: Track performance and costs over time

**Implementation**:

```python
# backend/utils/metrics.py (NEW FILE)
from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime
import json

@dataclass
class RequestMetrics:
    """Metrics for a single request."""
    request_id: str
    topic: str
    start_time: datetime
    end_time: datetime = None
    
    # Agent timings (ms)
    planner_duration: float = 0
    retriever_duration: float = 0
    summarizer_duration: float = 0
    verifier_duration: float = 0
    emailer_duration: float = 0
    
    # Token usage
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    
    # Costs
    total_cost: float = 0
    
    # Tool calls
    search_calls: int = 0
    email_calls: int = 0
    
    # Success
    success: bool = False
    error: str = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "request_id": self.request_id,
            "topic": self.topic,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "total_duration_ms": self.total_duration_ms,
            "agent_durations": {
                "planner": self.planner_duration,
                "retriever": self.retriever_duration,
                "summarizer": self.summarizer_duration,
                "verifier": self.verifier_duration,
                "emailer": self.emailer_duration
            },
            "tokens": {
                "input": self.total_input_tokens,
                "output": self.total_output_tokens,
                "total": self.total_input_tokens + self.total_output_tokens
            },
            "cost_usd": self.total_cost,
            "tool_calls": {
                "search": self.search_calls,
                "email": self.email_calls
            },
            "success": self.success,
            "error": self.error
        }
    
    @property
    def total_duration_ms(self) -> float:
        """Calculate total duration."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return 0
    
    def save_to_file(self):
        """Save metrics to file."""
        import os
        metrics_dir = "logs/metrics"
        os.makedirs(metrics_dir, exist_ok=True)
        
        filename = f"{metrics_dir}/{self.request_id}.json"
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)


class MetricsCollector:
    """Global metrics collector."""
    
    def __init__(self):
        self.current_metrics: Dict[str, RequestMetrics] = {}
    
    def start_request(self, request_id: str, topic: str) -> RequestMetrics:
        """Start tracking a request."""
        metrics = RequestMetrics(
            request_id=request_id,
            topic=topic,
            start_time=datetime.utcnow()
        )
        self.current_metrics[request_id] = metrics
        return metrics
    
    def end_request(self, request_id: str, success: bool = True, error: str = None):
        """End tracking a request."""
        if request_id in self.current_metrics:
            metrics = self.current_metrics[request_id]
            metrics.end_time = datetime.utcnow()
            metrics.success = success
            metrics.error = error
            
            # Save to file
            metrics.save_to_file()
            
            # Remove from active tracking
            del self.current_metrics[request_id]
    
    def get_metrics(self, request_id: str) -> RequestMetrics:
        """Get metrics for a request."""
        return self.current_metrics.get(request_id)


# Global instance
metrics_collector = MetricsCollector()
```

**Usage in workflow**:
```python
# backend/api/routes.py
from utils.metrics import metrics_collector
import time

async def event_generator():
    request_id = workflow_id
    
    # Start tracking
    metrics = metrics_collector.start_request(request_id, topic)
    
    try:
        # Track each agent
        start = time.time()
        # ... planner execution ...
        metrics.planner_duration = (time.time() - start) * 1000
        
        # ... similar for other agents ...
        
        # End tracking
        metrics_collector.end_request(request_id, success=True)
        
    except Exception as e:
        metrics_collector.end_request(request_id, success=False, error=str(e))
```

**Result**:
- ✅ Per-request metrics saved to files
- ✅ Can analyze performance trends
- ✅ Can calculate costs

**Effort**: 20 minutes  
**Impact**: 🔥 MEDIUM - Good for analysis

---

## 📊 Summary: What to Implement

### Immediate (Do Today - 30 minutes total)

| Enhancement | Effort | Impact | What You Get |
|-------------|--------|--------|--------------|
| **1. LangSmith Tracing** | 5 min | 🔥🔥🔥 | Full LLM visibility, token tracking, cost calculation |
| **2. Request ID Tracking** | 10 min | 🔥🔥 | Correlation across logs, easier debugging |
| **3. Structured Logging** | 15 min | 🔥🔥 | Machine-readable logs, metrics extraction |

**Total**: 30 minutes for massive observability improvement

### This Week (1-2 hours)

| Enhancement | Effort | Impact | What You Get |
|-------------|--------|--------|--------------|
| **4. Metrics Tracking** | 20 min | 🔥 | Per-request metrics, performance analysis |
| **5. Cost Dashboard** | 30 min | 🔥 | Real-time cost monitoring |
| **6. Latency Dashboard** | 30 min | 🔥 | Performance bottleneck identification |

---

## 🎯 Recommended Implementation Order

### Phase 1: LangSmith (5 minutes) ⭐ DO THIS FIRST
```bash
# 1. Add to .env
LANGSMITH_API_KEY=lsv2_pt_your_key_here

# 2. Add @traceable to agents (5 decorators)
# 3. Done! Check https://smith.langchain.com/
```

**Why First**: Zero code changes, instant full observability

### Phase 2: Request Tracking (10 minutes)
```bash
# 1. Create middleware file
# 2. Add to main.py
# 3. Update logger format
```

**Why Second**: Makes debugging much easier

### Phase 3: Structured Logging (15 minutes)
```bash
# 1. Create structured_logger.py
# 2. Update agents to use it
# 3. Add log parsing scripts
```

**Why Third**: Enables metrics and dashboards

### Phase 4: Metrics Collection (20 minutes)
```bash
# 1. Create metrics.py
# 2. Integrate into workflow
# 3. Create simple dashboard
```

**Why Fourth**: Builds on structured logs

---

## 📈 What You'll Have After Implementation

### With LangSmith Only (5 minutes)
- ✅ Full trace of every request
- ✅ All LLM calls with prompts/responses
- ✅ Token usage per call
- ✅ Cost per request
- ✅ Latency per agent
- ✅ Error tracking
- ✅ Searchable traces
- ✅ Cost trends over time

### With All Quick Wins (30 minutes)
- ✅ Everything above PLUS:
- ✅ Request ID correlation
- ✅ Structured JSON logs
- ✅ Per-request metrics files
- ✅ Easy log parsing
- ✅ Performance analytics

---

## 🚫 What NOT to Do (Avoid Over-Engineering)

❌ Don't build custom dashboards (use LangSmith)  
❌ Don't implement custom token counting (LangSmith does it)  
❌ Don't build custom trace visualization (LangSmith has it)  
❌ Don't set up Prometheus/Grafana yet (overkill for now)  
❌ Don't build custom cost tracking (LangSmith calculates it)  

**Key Insight**: LangSmith gives you 80% of what you need with 5 minutes of work!

---

## 📋 Implementation Checklist

### LangSmith Setup (5 min)
- [ ] Get LangSmith API key from https://smith.langchain.com/
- [ ] Add `LANGSMITH_API_KEY` to `.env`
- [ ] Add `@traceable` to `plan_research()`
- [ ] Add `@traceable` to `retrieve_information()`
- [ ] Add `@traceable` to `summarize_research()`
- [ ] Add `@traceable` to `verify_research()`
- [ ] Add `@traceable` to `send_research_email()`
- [ ] Add `@traceable` to `run_research_workflow()`
- [ ] Test: Run a research request
- [ ] Verify: Check LangSmith dashboard for traces

### Request ID Tracking (10 min)
- [ ] Create `backend/api/middleware/request_id.py`
- [ ] Add middleware to `main.py`
- [ ] Update logger formatter to include request_id
- [ ] Test: Check logs for request IDs

### Structured Logging (15 min)
- [ ] Create `backend/utils/structured_logger.py`
- [ ] Update agents to use structured logger
- [ ] Test: Check logs for JSON format
- [ ] Create log parsing script (optional)

### Metrics Tracking (20 min)
- [ ] Create `backend/utils/metrics.py`
- [ ] Integrate into workflow
- [ ] Test: Check `logs/metrics/` for JSON files
- [ ] Create simple dashboard (optional)

---

## 🎓 Learning Resources

**LangSmith Documentation**:
- https://docs.smith.langchain.com/
- https://docs.smith.langchain.com/tracing
- https://docs.smith.langchain.com/evaluation

**Python Logging**:
- https://docs.python.org/3/library/logging.html
- https://docs.python.org/3/howto/logging-cookbook.html

---

## 💡 Next Steps

1. **Start with LangSmith** (5 minutes)
   - Instant full observability
   - No code changes needed
   - Massive value

2. **Add Request IDs** (10 minutes)
   - Better debugging
   - Log correlation

3. **Structured Logging** (15 minutes)
   - Machine-readable logs
   - Enable analytics

4. **Review in LangSmith**
   - See what you're getting
   - Decide what else you need

**Total Time**: 30 minutes for production-grade observability! 🚀
