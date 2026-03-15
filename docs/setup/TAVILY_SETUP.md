# Tavily AI Search Setup Guide

**FREE alternative to Brave Search - 1,000 searches/month, no credit card required!**

---

## 🎯 Why Tavily?

Brave Search API now requires a paid subscription. **Tavily AI** is a better alternative:

✅ **1,000 FREE searches/month** (vs Brave's paid-only model)  
✅ **No credit card required**  
✅ **Instant API key** (no waiting)  
✅ **AI-optimized results** (designed for LLM agents)  
✅ **Clean, structured data** (perfect for our use case)  
✅ **Better for research** than raw search results  

---

## 🚀 Quick Setup (2 minutes)

### **Step 1: Sign Up**
1. Go to: **https://tavily.com**
2. Click "Get Started" or "Sign Up"
3. Sign up with:
   - Email + password, OR
   - Google account, OR
   - GitHub account

### **Step 2: Get API Key**
1. After signup, you'll be redirected to the dashboard
2. Your API key is **immediately visible** on the dashboard
3. Copy the key (starts with `tvly-`)

### **Step 3: Add to `.env`**
```bash
# Open your .env file
cd /Volumes/WorkSpace/Projects/InterviewPreps/MCPAIResearchAgent

# Add this line:
TAVILY_API_KEY=tvly-your-actual-key-here
```

### **Step 4: Test It**
```bash
# Start backend
cd backend
source venv/bin/activate
python api/main.py

# In another terminal, test:
curl http://localhost:8000/health
```

---

## 📊 Tavily vs Brave Comparison

| Feature | Tavily (FREE) | Brave Search |
|---------|---------------|--------------|
| **Cost** | $0 | Requires paid plan |
| **Free Queries** | 1,000/month | 0 (no free tier) |
| **Credit Card** | Not required | Required |
| **Setup Time** | 2 minutes | N/A (paid only) |
| **AI-Optimized** | ✅ Yes | ❌ No |
| **For LLM Agents** | ✅ Designed for it | ❌ General search |

---

## 💡 What Changed in the Code?

We updated `backend/mcp_tools/search_tool.py` to use Tavily's REST API directly:

**Before** (Brave Search via MCP):
```python
# Used MCP subprocess to call Brave Search
client = MCPClient(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-brave-search"],
    env={"BRAVE_API_KEY": self.api_key}
)
```

**After** (Tavily direct API):
```python
# Direct HTTP call to Tavily API
async with httpx.AsyncClient() as client:
    response = await client.post(
        "https://api.tavily.com/search",
        json={
            "api_key": self.api_key,
            "query": query,
            "max_results": count
        }
    )
```

**Benefits**:
- ✅ No MCP server needed for search (simpler)
- ✅ Faster (direct API call)
- ✅ More reliable (no subprocess overhead)
- ✅ Better results (AI-optimized)

---

## 🧪 Test Your Setup

After adding the API key, test the search tool:

```python
# In Python shell
cd backend
source venv/bin/activate
python

# Test search
import asyncio
from mcp_tools.search_tool import SearchMCPTool

async def test():
    search = SearchMCPTool()
    results = await search.web_search("quantum computing", count=3)
    for r in results:
        print(f"Title: {r['title']}")
        print(f"URL: {r['url']}")
        print(f"Content: {r['content'][:100]}...")
        print("---")

asyncio.run(test())
```

Expected output:
```
Title: Quantum Computing Explained
URL: https://example.com/quantum
Content: Quantum computing is a revolutionary technology...
---
```

---

## 📈 Usage Monitoring

### **Check Your Usage**
1. Go to: https://app.tavily.com/dashboard
2. View "API Usage" section
3. See queries used / 1,000 limit

### **Usage Estimate for This Project**
- **Per research**: 3-5 queries (sub-queries from Planner)
- **100 test researches**: 300-500 queries
- **Remaining**: 500-700 queries for more testing

**You have plenty of headroom!** 🎉

---

## 🔄 If You Need More Queries

### **Upgrade Options** (if you exceed 1,000/month)
- **Pro Plan**: $100/month for 100,000 queries
- **Enterprise**: Custom pricing

**For this learning project**: Free tier is more than enough!

---

## 🆘 Troubleshooting

### **"TAVILY_API_KEY not set" Error**
```bash
# Check .env file exists
ls -la .env

# Check key is set
cat .env | grep TAVILY

# Restart backend to reload .env
# Ctrl+C to stop, then:
python api/main.py
```

### **"Invalid API key" Error**
- Verify key starts with `tvly-`
- No extra spaces in .env
- No quotes around the key
- Key is active on Tavily dashboard

### **"Rate limit exceeded" Error**
- Check usage on dashboard
- You've used 1,000 queries this month
- Wait for monthly reset or upgrade

---

## ✅ Summary

**Tavily is the perfect free alternative to Brave Search!**

- ✅ Setup in 2 minutes
- ✅ No credit card
- ✅ 1,000 free searches/month
- ✅ Better for AI agents
- ✅ Already integrated in your code

**Next Steps**:
1. Sign up at https://tavily.com
2. Copy your API key
3. Add to `.env` file
4. Start testing your research agent!

---

**Happy researching!** 🚀
