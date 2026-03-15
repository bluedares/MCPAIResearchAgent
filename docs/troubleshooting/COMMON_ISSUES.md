# 🔧 Common Issues & Solutions

Quick solutions to common problems with the MCP Research Agent.

---

## 🚨 **Backend Issues**

### **Issue: Backend won't start**

**Symptoms:**
```bash
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# Activate virtual environment
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep fastapi
```

---

### **Issue: API key errors**

**Symptoms:**
```bash
AuthenticationError: Invalid API key
```

**Solution:**
```bash
# Check .env file exists
ls backend/.env

# Verify API keys are set
cat backend/.env | grep API_KEY

# Get new keys if needed
# Anthropic: https://console.anthropic.com/
# Tavily: https://tavily.com/
```

**Correct format:**
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
TAVILY_API_KEY=tvly-...
```

---

### **Issue: Port already in use**

**Symptoms:**
```bash
ERROR: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
uvicorn api.main:app --port 8001
```

---

### **Issue: Import errors**

**Symptoms:**
```bash
ImportError: cannot import name 'settings'
```

**Solution:**
```bash
# Ensure you're in backend directory
cd backend

# Check Python path
python -c "import sys; print(sys.path)"

# Run with correct path
PYTHONPATH=. uvicorn api.main:app --reload
```

---

## 🌐 **Frontend Issues**

### **Issue: Frontend won't start**

**Symptoms:**
```bash
Error: Cannot find module 'vite'
```

**Solution:**
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Start dev server
npm run dev
```

---

### **Issue: CORS errors**

**Symptoms:**
```
Access to fetch blocked by CORS policy
```

**Solution:**
```python
# In backend/config/settings.py
cors_origins = "http://localhost:5173,http://localhost:3000"

# Restart backend
```

**Verify:**
```bash
curl -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: POST" \
  -X OPTIONS http://localhost:8000/api/config
```

---

### **Issue: Connection refused**

**Symptoms:**
```
Failed to fetch: Connection refused
```

**Solution:**
```bash
# Check backend is running
curl http://localhost:8000/api/config

# If not running, start backend
cd backend
uvicorn api.main:app --reload

# Check correct port in frontend
# frontend/src/App.tsx should use http://localhost:8000
```

---

## 🔄 **Workflow Issues**

### **Issue: Validation always fails**

**Symptoms:**
```
All topics rejected as "too vague"
```

**Solution:**
```bash
# Check topic length
# Must be 10-500 characters

# Be specific
❌ "AI"
✅ "Latest AI developments in healthcare 2026"

# Check API key
# Validator uses Claude - verify ANTHROPIC_API_KEY
```

---

### **Issue: Workflow stuck on "Planning"**

**Symptoms:**
```
Progress stuck at "Planning research strategy..."
```

**Solution:**
```bash
# Check backend logs
tail -f backend/logs/research_agent.log

# Look for errors
grep "ERROR" backend/logs/research_agent.log

# Common causes:
# 1. Anthropic API rate limit
# 2. Network timeout
# 3. Invalid API key

# Restart workflow
```

---

### **Issue: No search results**

**Symptoms:**
```
Retriever returns empty results
```

**Solution:**
```bash
# Check Tavily API key
echo $TAVILY_API_KEY

# Test Tavily directly
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d '{"api_key":"YOUR_KEY","query":"test"}'

# Check logs
grep "Tavily" backend/logs/agents.log
```

---

### **Issue: Summary is empty**

**Symptoms:**
```
Complete event has empty summary
```

**Solution:**
```bash
# Check logs for summarizer errors
grep "summarizer" backend/logs/agents.log

# Common causes:
# 1. No search results
# 2. Claude API error
# 3. Structured output parsing failed

# Fallback should generate text summary
# If not, check backend/agents/summarizer.py
```

---

### **Issue: Infinite retry loop**

**Symptoms:**
```
Workflow keeps retrying verification
```

**Solution:**
```bash
# Check retry count in logs
grep "retry_count" backend/logs/workflow.log

# Circuit breaker should force pass after 1 retry
# If not working, check backend/graph/workflow.py

# Verify should_retry_summary function
```

**Expected behavior:**
```
Attempt 1: Verify → Fail → Retry
Attempt 2: Verify → Fail → Force Pass → Continue
```

---

## 📧 **Email Issues**

### **Issue: Email not sending**

**Symptoms:**
```
Email sent: false
```

**Solution:**
```bash
# Check EMAIL_ENABLED flag
grep EMAIL_ENABLED backend/.env

# Should be:
EMAIL_ENABLED=true

# Restart backend after changing
```

---

### **Issue: Email UI not showing**

**Symptoms:**
```
No email input in form
```

**Solution:**
```bash
# Check frontend fetched config
# Open browser console
# Should see: GET /api/config → {email_enabled: true}

# If false, set in backend/.env:
EMAIL_ENABLED=true

# Restart backend
# Refresh browser
```

---

## 💾 **Caching Issues**

### **Issue: Redis connection failed**

**Symptoms:**
```
Redis not configured, caching disabled
```

**Solution:**
```bash
# Install Redis
brew install redis  # macOS
sudo apt install redis  # Linux

# Start Redis
redis-server

# Test connection
redis-cli ping  # Should return PONG

# Set in .env
REDIS_URL=redis://localhost:6379

# Restart backend
```

---

### **Issue: Cache not working**

**Symptoms:**
```
Same query always re-executes workflow
```

**Solution:**
```bash
# Check Redis is running
redis-cli ping

# Check cache keys
redis-cli KEYS "research:*"

# Check logs
grep "cache" backend/logs/research_agent.log

# Should see:
# "Cache MISS" on first query
# "Cache HIT" on repeat query
```

---

## 🔍 **Debugging Tips**

### **Enable Verbose Logging**

```python
# In backend/config/settings.py
debug = True

# In backend/utils/logger.py
logging.basicConfig(level=logging.DEBUG)
```

### **Check LangSmith Traces**

```bash
# Set in .env
LANGSMITH_API_KEY=ls-...
LANGSMITH_TRACING_V2=true

# Visit https://smith.langchain.com/
# View traces for your project
```

### **Test Individual Agents**

```python
# Test validator
from agents.topic_validator import validate_topic
result = await validate_topic("Latest AI developments")
print(result)

# Test planner
from agents.planner import plan_research
result = await plan_research("Latest AI developments")
print(result)
```

### **Monitor API Calls**

```bash
# Watch logs in real-time
tail -f backend/logs/research_agent.log | grep "API"

# Count API calls
grep "Anthropic API" backend/logs/research_agent.log | wc -l
```

---

## 🆘 **Still Having Issues?**

1. **Check logs:**
   ```bash
   tail -100 backend/logs/research_agent.log
   ```

2. **Verify environment:**
   ```bash
   python --version  # Should be 3.9+
   node --version    # Should be 18+
   ```

3. **Check dependencies:**
   ```bash
   pip list | grep langchain
   npm list | grep vite
   ```

4. **Review configuration:**
   ```bash
   cat backend/.env
   ```

5. **Test API endpoints:**
   ```bash
   curl http://localhost:8000/api/config
   ```

6. **See detailed guides:**
   - [Debug Guide](./DEBUG_GUIDE.md)
   - [Setup Guide](../setup/DEVELOPMENT_SETUP.md)
   - [API Docs](../api/ENDPOINTS.md)

---

## 📞 **Get Help**

- **Documentation**: Check all docs in `/docs`
- **Logs**: Always check logs first
- **LangSmith**: View traces for AI calls
- **GitHub Issues**: Report bugs

---

**Last Updated:** March 2026
