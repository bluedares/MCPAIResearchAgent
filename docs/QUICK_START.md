# ⚡ Quick Start Guide

Get the MCP Research Agent running in **5 minutes**!

---

## 📋 **Prerequisites**

- Python 3.9+
- Node.js 18+
- Anthropic API Key
- Tavily API Key

---

## 🚀 **5-Minute Setup**

### **Step 1: Clone & Install (2 minutes)**

```bash
# Clone repository
git clone <repo-url>
cd MCPAIResearchAgent

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup (new terminal)
cd frontend
npm install
```

### **Step 2: Configure API Keys (1 minute)**

```bash
# In backend directory
cp .env.example .env
```

Edit `backend/.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
TAVILY_API_KEY=tvly-your-key-here
```

### **Step 3: Start Services (1 minute)**

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn api.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### **Step 4: Test (1 minute)**

1. Open http://localhost:5173
2. Enter topic: `"Latest developments in quantum computing"`
3. Click **Start Research**
4. Watch the magic happen! ✨

---

## 🎯 **What Happens Next?**

```
Your Query
    ↓
Validation (1s)
    ↓
Planning (3s)
    ↓
Searching (5-10s)
    ↓
Summarizing (15-20s)
    ↓
Verifying (5s)
    ↓
Results! 🎉
```

**Total time:** 30-60 seconds

---

## 🛡️ **Try the Guardrails**

Test input validation:

❌ **These will be rejected:**
- "What is my name?"
- "AI"
- "the latest"

✅ **These will work:**
- "Latest AI developments in 2026"
- "History of quantum computing"
- "Best practices for React development"

---

## 📊 **View Logs**

```bash
cd backend
tail -f logs/research_agent.log
```

---

## 🔧 **Optional Features**

### **Enable Email Sending**

```bash
# In backend/.env
EMAIL_ENABLED=true
```

### **Enable Redis Caching**

```bash
# Install Redis
brew install redis  # macOS
redis-server

# In backend/.env
REDIS_URL=redis://localhost:6379
```

---

## 🆘 **Troubleshooting**

**Backend won't start?**
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install -r requirements.txt
```

**Frontend won't start?**
```bash
# Check Node version
node --version  # Should be 18+

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**API errors?**
- Verify API keys in `backend/.env`
- Check API key validity at provider websites

---

## 📚 **Next Steps**

- [Architecture Overview](./architecture/OVERVIEW.md) - Understand the system
- [Workflow Guide](./guides/WORKFLOW_GUIDE.md) - Deep dive into the workflow
- [API Documentation](./api/ENDPOINTS.md) - API reference
- [Debug Guide](./troubleshooting/DEBUG_GUIDE.md) - Debugging tips

---

**You're all set! Happy researching! 🚀**
