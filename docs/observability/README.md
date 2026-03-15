# Observability Documentation

This folder contains all observability and monitoring documentation for the MCP AI Research Agent.

## 📁 Files in This Folder

### [LANGSMITH_IMPLEMENTATION.md](./LANGSMITH_IMPLEMENTATION.md)
Complete implementation guide for LangSmith observability.

**Contents**:
- What was implemented (6 files modified)
- Changes made to each agent
- Environment variables configuration
- What you get with LangSmith tracing
- Example trace outputs
- How to use LangSmith dashboard
- Debugging capabilities
- Cost analytics
- Performance monitoring

**Use when**: Understanding the LangSmith implementation or viewing traces

---

### [OBSERVABILITY_AUDIT.md](./OBSERVABILITY_AUDIT.md)
Comprehensive audit of current observability implementation and recommendations.

**Contents**:
- Current implementation review
- What's already implemented vs missing
- Critical gaps analysis
- Quick wins (minimal code changes)
  - Priority 1: LangSmith Tracing (5 min) ⭐
  - Priority 2: Request ID Tracking (10 min)
  - Priority 3: Structured Logging (15 min)
  - Priority 4: Metrics Tracking (20 min)
- Implementation examples with code
- What NOT to do (avoid over-engineering)
- Implementation checklist

**Use when**: Planning observability improvements or implementing monitoring

---

## 🔍 Observability Stack

### Current Implementation

✅ **LangSmith Tracing** - Full LLM observability
- Every LLM call traced
- Prompts and responses logged
- Token usage tracked
- Costs calculated automatically
- Latency measured per agent
- Error tracking with context

✅ **Basic Logging** - File-based logging
- 3 separate log files (research_agent.log, agents.log, workflow.log)
- Console + file logging
- Agent-specific loggers

✅ **Status Messages** - Real-time progress
- Workflow state tracking
- Streamed to frontend via SSE

### Recommended Additions

See [OBSERVABILITY_AUDIT.md](./OBSERVABILITY_AUDIT.md) for:
- Request ID tracking
- Structured JSON logging
- Metrics collection
- Cost dashboards
- Latency monitoring

---

## 🚀 Quick Start

### View LangSmith Traces

1. **Ensure LangSmith is configured**:
   ```bash
   # Check backend/.env
   LANGSMITH_API_KEY=lsv2_pt_...
   LANGSMITH_PROJECT=mcp-research-agent
   LANGSMITH_TRACING_V2=true
   ```

2. **Run a research request**:
   - Start backend and frontend
   - Submit a research topic
   - Wait for completion

3. **View traces**:
   - Go to https://smith.langchain.com/
   - Select project: `mcp-research-agent`
   - See full trace with all agents

### What You'll See

```
research_workflow (7.9s, $0.210)
├─ planner_agent (1.2s, $0.027, 700 tokens)
├─ retriever_agent (2.3s, 5 searches)
├─ summarizer_agent (3.1s, $0.138, 3800 tokens)
├─ verifier_agent (0.8s, $0.045, 1350 tokens)
└─ email_sender_agent (0.5s, email sent ✓)
```

---

## 📊 Key Metrics Tracked

### Automatic (via LangSmith)
- ✅ Request logs
- ✅ Prompt logs
- ✅ Tool execution logs
- ✅ Latency tracking
- ✅ Token usage metrics
- ✅ Cost monitoring

### Manual (via logging)
- ✅ Application startup
- ✅ Environment configuration
- ✅ Agent execution steps
- ✅ Workflow state transitions

---

## 🎯 Observability Checklist

- [x] LangSmith tracing enabled
- [x] Basic logging configured
- [x] Status messages implemented
- [ ] Request ID tracking (optional)
- [ ] Structured JSON logging (optional)
- [ ] Metrics collection (optional)
- [ ] Cost alerts (optional)
- [ ] Performance baselines (optional)

---

## 📖 Related Documentation

- [Deployment](../deployment/) - Production deployment guides
- [Architecture](../architecture/) - System architecture
- [Guides](../guides/) - Agent and workflow guides
- [Setup](../setup/) - Local development setup

---

## 💡 Best Practices

1. **Always check LangSmith** after deploying changes
2. **Monitor costs** regularly to avoid surprises
3. **Review traces** for failed requests to debug issues
4. **Track latency trends** to identify performance degradation
5. **Use structured logging** for production environments

---

**LangSmith Dashboard**: https://smith.langchain.com/  
**Project**: `mcp-research-agent`
