# 🚀 Redis Caching Implementation

## 📋 **Overview**

Redis caching is implemented to avoid redundant API calls for duplicate research topics. When a user searches for the same topic, results are served from cache instantly.

---

## ⚡ **Benefits**

| Benefit | Impact |
|---------|--------|
| **Speed** | Instant results (< 100ms vs 30-60s) |
| **Cost Savings** | No Anthropic API calls ($0.20-0.30 saved per cached request) |
| **Tavily API** | No search API calls (saves quota) |
| **User Experience** | Immediate response for repeat queries |

---

## 🔧 **How It Works**

### **1. Cache Key Generation**
```python
# Topic is normalized and hashed
topic = "Latest AI Developments"
normalized = "latest ai developments"  # lowercase, stripped
hash = md5(normalized)[:12]  # "a1b2c3d4e5f6"
cache_key = "research:a1b2c3d4e5f6"
```

### **2. Cache Flow**

```
User Request
    ↓
Check Redis Cache
    ↓
┌─────────────┬─────────────┐
│  Cache HIT  │  Cache MISS │
└─────────────┴─────────────┘
      ↓              ↓
Return Cached    Run Full
  (instant)      Workflow
                (30-60s)
                    ↓
                Cache Result
                (24h TTL)
```

### **3. What Gets Cached**

```json
{
  "topic": "Latest AI Developments",
  "summary": "Full research summary...",
  "citations": [
    {
      "claim": "...",
      "source_url": "...",
      "source_title": "..."
    }
  ],
  "verified": true,
  "cached_at": "24 hours"
}
```

---

## 🎯 **Cache Strategy**

### **Cache Key Components**
- **Topic hash**: MD5 hash of normalized topic (12 chars)
- **Email hash** (optional): For personalized results
- **Format**: `research:{topic_hash}` or `research:{topic_hash}:{email_hash}`

### **TTL (Time To Live)**
- **Default**: 24 hours
- **Rationale**: Research stays relevant for a day, then refreshes

### **Cache Invalidation**
- Automatic after 24 hours
- Manual via API endpoint (future feature)

---

## 📊 **Performance Comparison**

| Scenario | Without Cache | With Cache | Savings |
|----------|---------------|------------|---------|
| **Time** | 30-60 seconds | < 100ms | **99.8%** |
| **Anthropic API** | $0.20-0.30 | $0.00 | **100%** |
| **Tavily API** | 5-10 searches | 0 searches | **100%** |
| **User Wait** | 30-60s | Instant | **Instant** |

---

## 🔍 **Cache Monitoring**

### **View Cache Stats**
```bash
# In Python console
from utils.redis_cache import get_cache_stats
stats = get_cache_stats()
print(stats)
```

**Output:**
```json
{
  "enabled": true,
  "total_keys": 42,
  "hits": 156,
  "misses": 89,
  "hit_rate": 0.64
}
```

### **Check Logs**
```bash
tail -f backend/logs/research_agent.log | grep -E "Cache|cache"
```

**Example logs:**
```
✅ Cache HIT for topic: Latest AI developments...
❌ Cache MISS for topic: Quantum computing advances...
✅ Cached research for topic: Quantum computing... (TTL: 24h)
```

---

## 🛠️ **Configuration**

### **Enable Redis**

**Option 1: Local Redis**
```bash
# Install Redis
brew install redis  # macOS
sudo apt install redis  # Linux

# Start Redis
redis-server

# Update .env
REDIS_URL=redis://localhost:6379
```

**Option 2: Railway Redis (Production)**
```bash
# Railway auto-injects
RAILWAY_REDIS_URL=redis://...
```

**Option 3: Upstash Redis (Serverless)**
```bash
# Get free Redis at https://upstash.com
REDIS_URL=redis://...@upstash.io:6379
```

### **Disable Caching**
```bash
# In .env - comment out or remove
# REDIS_URL=redis://localhost:6379
```

---

## 🧪 **Testing Cache**

### **Test 1: Cache Miss → Hit**
```bash
# First request (cache miss)
curl -X GET "http://localhost:8000/api/research/test-1/stream?topic=AI%20trends&client_email="

# Second request (cache hit - instant!)
curl -X GET "http://localhost:8000/api/research/test-2/stream?topic=AI%20trends&client_email="
```

### **Test 2: Different Topics**
```bash
# Different topics = different cache keys
curl "...?topic=AI%20trends"  # Cache key: research:a1b2c3...
curl "...?topic=Quantum%20computing"  # Cache key: research:d4e5f6...
```

### **Test 3: Same Topic, Different Email**
```bash
# Same topic, no email = shared cache
curl "...?topic=AI%20trends&client_email="

# Same topic, with email = separate cache (personalized)
curl "...?topic=AI%20trends&client_email=user@example.com"
```

---

## 📈 **Cache Hit Rate Goals**

| Scenario | Expected Hit Rate |
|----------|-------------------|
| **Development** | 20-30% (lots of testing) |
| **Production** | 40-60% (repeat queries) |
| **High Traffic** | 60-80% (popular topics) |

---

## 🔐 **Security Considerations**

### **Cache Isolation**
- Each email gets separate cache (if provided)
- No cross-user data leakage

### **Sensitive Data**
- Summaries are public research (safe to cache)
- No personal data cached
- Email addresses hashed in cache keys

### **Cache Poisoning Prevention**
- Topic normalized before hashing
- No user-controlled cache keys
- TTL ensures fresh data

---

## 🚨 **Troubleshooting**

### **Cache Not Working**

**Check 1: Redis Connection**
```bash
redis-cli ping
# Should return: PONG
```

**Check 2: Logs**
```bash
grep "Redis" backend/logs/research_agent.log
```

**Expected:**
```
✅ Redis cache initialized successfully
```

**If disabled:**
```
⏸️ Redis not configured, caching disabled
⚠️ Redis unavailable: Connection refused. Caching disabled.
```

### **Cache Not Clearing**

**Manual clear:**
```bash
redis-cli FLUSHDB  # Clear all keys in current database
```

**Clear specific topic:**
```python
from utils.redis_cache import invalidate_cache
await invalidate_cache("Latest AI developments")
```

---

## 📊 **Monitoring Dashboard (Future)**

Planned features:
- Real-time cache hit rate
- Most cached topics
- Cache size and memory usage
- Cache invalidation controls

---

## 🎯 **Summary**

**Current Implementation:**
- ✅ Automatic caching of research results
- ✅ 24-hour TTL
- ✅ Topic-based cache keys
- ✅ Graceful fallback if Redis unavailable
- ✅ Instant results for cached queries

**What Gets Cached:**
- ✅ Research summaries
- ✅ Citations
- ✅ Verification status
- ❌ NOT cached: Email sending, real-time data

**Performance:**
- ✅ 99.8% faster for cached queries
- ✅ 100% cost savings on cached requests
- ✅ No Tavily API calls for cached results

**Setup:**
- ✅ Works out of the box (disabled if no Redis)
- ✅ No code changes needed
- ✅ Just set `REDIS_URL` in `.env`

---

**Redis caching is now live! Repeat queries will be instant.** 🚀
