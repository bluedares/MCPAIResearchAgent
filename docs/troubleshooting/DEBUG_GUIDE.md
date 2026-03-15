# 🐛 Debug Guide - MCP Research Agent

## 📊 **Logging System**

### **Log Files Location**
All logs are stored in: `backend/logs/`

| Log File | Purpose | What You'll See |
|----------|---------|-----------------|
| `research_agent.log` | All application logs | Complete system activity |
| `agents.log` | Agent-specific logs | Planner, Retriever, Summarizer, Verifier, Email Sender |
| `workflow.log` | Workflow routing | State transitions, routing decisions |

---

## 🔍 **How to View Logs**

### **Real-Time Monitoring (Recommended)**

**Watch all activity:**
```bash
cd backend
tail -f logs/research_agent.log
```

**Watch only agents:**
```bash
tail -f logs/agents.log
```

**Watch workflow routing:**
```bash
tail -f logs/workflow.log
```

**Watch multiple logs simultaneously:**
```bash
tail -f logs/*.log
```

### **Search Logs**

**Find specific agent activity:**
```bash
grep "planner" logs/agents.log
grep "verifier" logs/agents.log
```

**Find errors:**
```bash
grep "ERROR" logs/research_agent.log
grep "WARNING" logs/research_agent.log
```

**Find specific workflow:**
```bash
grep "workflow-1773321958866" logs/research_agent.log
```

---

## 📝 **Log Format**

### **Standard Log Entry**
```
2026-03-12 19:05:01 | INFO | agents.planner:44 | 🧠 Planning research for: Latest AI developments
```

**Format breakdown:**
- `2026-03-12 19:05:01` - Timestamp
- `INFO` - Log level (DEBUG, INFO, WARNING, ERROR)
- `agents.planner:44` - Module and line number
- `🧠 Planning...` - Log message with emoji indicator

### **Emoji Indicators**

| Emoji | Meaning |
|-------|---------|
| 🧠 | Planning agent |
| 🔍 | Searching/Retriever agent |
| 📝 | Summarizing agent |
| ✅ | Verification agent |
| 📧 | Email sender agent |
| 🔀 | Workflow routing decision |
| 📊 | Metrics/statistics |
| ⚠️ | Warning |
| ❌ | Error |
| 🔄 | Retry attempt |

---

## 🎯 **Example Log Flow**

### **Successful Research Workflow**

```
2026-03-12 19:05:00 | INFO | 🚀 Starting research workflow
2026-03-12 19:05:01 | INFO | agents.planner:44 | 🧠 Planning research for: Latest AI developments
2026-03-12 19:05:02 | INFO | agents.planner:52 | ✅ Generated 5 sub-queries
2026-03-12 19:05:03 | INFO | agents.retriever:38 | 🔍 Searching for: AI breakthroughs 2024
2026-03-12 19:05:04 | INFO | agents.retriever:45 | ✅ Retrieved 15 results from 8 sources
2026-03-12 19:05:05 | INFO | agents.summarizer:44 | 📝 Synthesizing 15 results
2026-03-12 19:05:08 | INFO | agents.summarizer:67 | ✅ Created summary (1234 chars, 5 citations)
2026-03-12 19:05:09 | INFO | agents.verifier:44 | 🔍 Verifying summary (1234 chars, 5 citations)
2026-03-12 19:05:10 | INFO | agents.verifier:109 | 📊 Verification result: status=pass, confidence=0.85, retry_count=0
2026-03-12 19:05:10 | INFO | agents.verifier:126 | ✅ Verification passed
2026-03-12 19:05:11 | INFO | graph.workflow:120 | 🔀 Routing decision: status=pass, retry_count=0
2026-03-12 19:05:11 | INFO | graph.workflow:128 | ➡️ Proceeding to email sender
2026-03-12 19:05:12 | INFO | agents.email_sender:55 | 📧 Sending email to display@ui.local
2026-03-12 19:05:13 | INFO | ✅ Workflow complete
```

### **Workflow with Retry**

```
2026-03-12 19:10:09 | INFO | agents.verifier:44 | 🔍 Verifying summary (856 chars, 0 citations)
2026-03-12 19:10:10 | INFO | agents.verifier:109 | 📊 Verification result: status=fail, confidence=0.35, retry_count=0
2026-03-12 19:10:10 | WARNING | agents.verifier:139 | ⚠️ Verification failed (confidence: 0.35)
2026-03-12 19:10:11 | INFO | graph.workflow:120 | 🔀 Routing decision: status=fail, retry_count=0
2026-03-12 19:10:11 | INFO | graph.workflow:124 | 🔄 Retrying summarization (attempt 1)
2026-03-12 19:10:12 | INFO | agents.summarizer:44 | 📝 Synthesizing 15 results (retry 1)
2026-03-12 19:10:15 | INFO | agents.summarizer:67 | ✅ Created summary (1123 chars, 3 citations)
2026-03-12 19:10:16 | INFO | agents.verifier:44 | 🔍 Verifying summary (1123 chars, 3 citations)
2026-03-12 19:10:17 | WARNING | agents.verifier:113 | ⚠️ Max retries reached (1), forcing pass
2026-03-12 19:10:17 | INFO | graph.workflow:128 | ➡️ Proceeding to email sender
```

---

## 🔬 **LangSmith Tracing**

### **Access LangSmith Dashboard**
1. Visit: **https://smith.langchain.com/**
2. Login with your account
3. Select project: **mcp-research-agent**

### **What You Can See in LangSmith**

**Agent Traces:**
- Complete input/output for each agent
- LLM prompts sent to Claude
- Claude's responses
- Token usage and costs
- Execution time per agent

**Workflow Visualization:**
- Visual graph of workflow execution
- State transitions
- Conditional routing decisions
- Retry loops

**Performance Metrics:**
- Total execution time
- Token usage per agent
- Cost breakdown
- Success/failure rates

### **Example LangSmith Trace**

```
Research Workflow (45.2s, $0.23)
├─ Planner Agent (3.1s, $0.02)
│  ├─ Input: "Latest AI developments"
│  ├─ Prompt: "You are a research planning expert..."
│  ├─ Output: 5 sub-queries
│  └─ Tokens: 1,234 (in: 856, out: 378)
├─ Retriever Agent (8.5s, $0.05)
│  ├─ Tavily Search x5
│  └─ Results: 15 articles
├─ Summarizer Agent (25.3s, $0.12)
│  ├─ Input: 15 search results
│  ├─ Prompt: "Synthesize research findings..."
│  ├─ Output: 1,234 char summary + 5 citations
│  └─ Tokens: 8,456 (in: 6,234, out: 2,222)
├─ Verifier Agent (6.8s, $0.03)
│  ├─ Input: Summary + citations
│  ├─ Output: status=pass, confidence=0.85
│  └─ Tokens: 2,345 (in: 1,890, out: 455)
└─ Email Sender Agent (1.5s, $0.01)
   └─ Status: Skipped (display@ui.local)
```

---

## 🛠️ **Debugging Common Issues**

### **Issue 1: Infinite Loop (Summarizer ↔ Verifier)**

**Symptoms:**
- Workflow stuck in "Summarizing" and "Verifying" loop
- Same messages repeating

**Check logs:**
```bash
grep "retry_count" logs/workflow.log
```

**Expected behavior:**
- Max 1 retry
- After 1 retry, forces pass with "Not Verified" label

**If still looping:**
- Check `backend/graph/workflow.py:112-129` (routing logic)
- Check `backend/agents/verifier.py:112-123` (circuit breaker)

### **Issue 2: No Results Displayed**

**Symptoms:**
- Workflow completes but UI shows form again
- No summary or citations displayed

**Check logs:**
```bash
grep "complete" logs/research_agent.log
tail -20 logs/research_agent.log
```

**Verify SSE completion event:**
```bash
grep "type.*complete" logs/research_agent.log
```

**Should see:**
```json
{
  "type": "complete",
  "summary": "...",
  "citations": [...],
  "verified": true/false
}
```

### **Issue 3: API Key Errors**

**Symptoms:**
- "Could not resolve authentication method"
- "API key not set"

**Check configuration:**
```bash
cd backend
source venv/bin/activate
python -c "from config.settings import settings; print('Anthropic:', settings.anthropic_api_key[:20]); print('Tavily:', settings.tavily_api_key[:20])"
```

**Verify .env file:**
```bash
cat backend/.env | grep -E "ANTHROPIC|TAVILY"
```

### **Issue 4: Slow Performance**

**Check execution time per agent:**
```bash
grep "seconds" logs/agents.log
```

**Typical execution times:**
- Planner: 2-5 seconds
- Retriever: 5-10 seconds (depends on Tavily)
- Summarizer: 15-30 seconds (longest - Claude processing)
- Verifier: 5-10 seconds
- **Total: 30-60 seconds**

**If slower:**
- Check network latency to Anthropic/Tavily
- Check Claude API rate limits
- Monitor LangSmith for bottlenecks

---

## 📈 **Performance Monitoring**

### **Token Usage**

**View token consumption:**
```bash
grep "tokens" logs/agents.log
```

**Typical token usage per workflow:**
- Planner: ~1,000 tokens
- Summarizer: ~8,000 tokens (largest)
- Verifier: ~2,500 tokens
- **Total: ~12,000 tokens per research**

**Cost estimate:**
- Claude Sonnet 4: ~$0.20-0.30 per research
- Tavily: Free (1000 searches/month)

### **Success Rate**

**Count successful workflows:**
```bash
grep "Workflow complete" logs/research_agent.log | wc -l
```

**Count failed workflows:**
```bash
grep "ERROR" logs/research_agent.log | wc -l
```

**Verification pass rate:**
```bash
grep "Verification: PASS" logs/agents.log | wc -l
```

---

## 🔧 **Advanced Debugging**

### **Enable Verbose Logging**

Edit `backend/utils/logger.py`:
```python
# Change log level to DEBUG
log_level = logging.DEBUG  # Always debug mode
```

### **Add Custom Log Points**

In any agent file:
```python
import logging
logger = logging.getLogger(__name__)

logger.debug(f"🔍 Debug info: {variable}")
logger.info(f"✅ Important event: {data}")
logger.warning(f"⚠️ Warning: {issue}")
logger.error(f"❌ Error: {error}")
```

### **Trace Specific Workflow**

```bash
# Get workflow ID from UI or logs
WORKFLOW_ID="workflow-1773321958866"

# View all logs for this workflow
grep "$WORKFLOW_ID" logs/research_agent.log
```

---

## 📞 **Quick Reference**

### **Most Useful Commands**

```bash
# Watch live logs (Press Ctrl+C to exit)
tail -f logs/research_agent.log

# Find errors
grep "ERROR\|WARNING" logs/research_agent.log

# Check last workflow
tail -100 logs/research_agent.log

# Count workflows today
grep "Starting research workflow" logs/research_agent.log | grep "$(date +%Y-%m-%d)" | wc -l

# View verification results
grep "Verification result" logs/agents.log

# Check retry attempts
grep "retry_count" logs/workflow.log
```

---

## 💻 **Terminal Commands Guide**

### **Basic Log Viewing**

**View entire log file:**
```bash
cd backend
cat logs/research_agent.log
```

**View last 50 lines:**
```bash
tail -50 logs/research_agent.log
```

**View last 100 lines:**
```bash
tail -100 logs/research_agent.log
```

**Watch logs in real-time:**
```bash
tail -f logs/research_agent.log
# Press Ctrl+C to exit
```

---

### **Filtering Logs**

**Search for specific text:**
```bash
# Find all errors
grep "ERROR" logs/research_agent.log

# Find warnings
grep "WARNING" logs/research_agent.log

# Find both errors and warnings
grep -E "ERROR|WARNING" logs/research_agent.log
```

**Filter by agent:**
```bash
# Planner logs
grep "planner" logs/agents.log

# Summarizer logs
grep "summarizer" logs/agents.log

# Verifier logs
grep "verifier" logs/agents.log
```

**Filter by workflow ID:**
```bash
# Replace with your workflow ID
grep "workflow-1773324155442" logs/research_agent.log
```

---

### **Real-Time Filtered Logs**

**Watch specific events (emojis may not display in grep):**
```bash
# Watch completion events
tail -f logs/research_agent.log | grep "completion"

# Watch email events
tail -f logs/research_agent.log | grep "email"

# Watch verification
tail -f logs/research_agent.log | grep "verif"

# Watch all agent activity
tail -f logs/agents.log

# Press Ctrl+C to exit any of these
```

**Note**: Emoji filtering with grep may not work reliably. Instead, use:
```bash
# Watch all logs (emojis display correctly)
tail -f logs/research_agent.log

# Or filter by text keywords
tail -f logs/research_agent.log | grep -E "Sending completion|Email sender|Summarizer"
```

---

### **Exit Commands**

| Command | How to Exit |
|---------|-------------|
| `tail -f` | Press **Ctrl+C** |
| `grep` (running) | Press **Ctrl+C** |
| `less` (pager) | Press **q** |
| `vim` (editor) | Press **:q** then **Enter** |
| Terminal stuck | Press **Ctrl+C** or **Ctrl+D** |

---

### **Combining Commands**

**Search and count:**
```bash
# Count errors
grep "ERROR" logs/research_agent.log | wc -l

# Count successful workflows
grep "Workflow complete" logs/research_agent.log | wc -l
```

**Search with context:**
```bash
# Show 5 lines before and after error
grep -A 5 -B 5 "ERROR" logs/research_agent.log

# Show 10 lines after verification
grep -A 10 "Verification result" logs/agents.log
```

**Search in multiple files:**
```bash
# Search all log files
grep "ERROR" logs/*.log

# Search with filename display
grep -H "verification" logs/*.log
```

---

### **Time-Based Filtering**

**Today's logs:**
```bash
# Get today's date in YYYY-MM-DD format
TODAY=$(date +%Y-%m-%d)

# Filter today's logs
grep "$TODAY" logs/research_agent.log
```

**Last hour:**
```bash
# Get current hour
HOUR=$(date +%H)

# Filter by hour (approximate)
grep "$(date +%Y-%m-%d) $HOUR:" logs/research_agent.log
```

**Specific time range:**
```bash
# Between 19:00 and 20:00
grep "2026-03-12 19:" logs/research_agent.log
```

---

### **Log Analysis**

**Most common errors:**
```bash
grep "ERROR" logs/research_agent.log | sort | uniq -c | sort -rn
```

**Workflow statistics:**
```bash
echo "Total workflows:"
grep "Starting research workflow" logs/research_agent.log | wc -l

echo "Completed workflows:"
grep "Workflow complete" logs/research_agent.log | wc -l

echo "Failed workflows:"
grep "ERROR" logs/research_agent.log | wc -l
```

**Average verification confidence:**
```bash
grep "confidence:" logs/agents.log | grep -oE "confidence: [0-9.]+" | awk '{sum+=$2; count++} END {print "Average:", sum/count}'
```

---

### **Clearing Logs**

**Backup before clearing:**
```bash
# Create backup
cp logs/research_agent.log logs/research_agent.log.backup.$(date +%Y%m%d)

# Clear log file
> logs/research_agent.log
# OR
echo "" > logs/research_agent.log
```

**Delete all logs:**
```bash
# Delete all log files (use with caution!)
rm logs/*.log
```

**Rotate logs:**
```bash
# Move old logs to archive
mkdir -p logs/archive
mv logs/*.log logs/archive/$(date +%Y%m%d)/
```

---

### **Troubleshooting Commands**

**Check if backend is running:**
```bash
# Check process
ps aux | grep uvicorn

# Check port
lsof -i :8000
```

**Check Redis connection:**
```bash
# Ping Redis
redis-cli ping
# Should return: PONG

# Check Redis keys
redis-cli KEYS "research:*"
```

**Check disk space:**
```bash
# Check log directory size
du -sh logs/

# Check available disk space
df -h
```

**Check file permissions:**
```bash
# List log files with permissions
ls -lh logs/
```

### **Log Rotation**

Logs are appended indefinitely. To clear:
```bash
# Backup old logs
mv logs/research_agent.log logs/research_agent.log.backup

# Or delete all logs
rm logs/*.log
```

---

## 🎯 **Summary**

**For Real-Time Debugging:**
```bash
tail -f backend/logs/research_agent.log
```

**For Deep Analysis:**
- Use LangSmith: https://smith.langchain.com/
- Check `backend/logs/agents.log` for agent details
- Check `backend/logs/workflow.log` for routing decisions

**For Performance:**
- Monitor token usage in LangSmith
- Check execution times in logs
- Verify API response times

**For Errors:**
- Search logs for ERROR/WARNING
- Check state transitions in workflow.log
- Verify API keys in settings
