# API Keys Setup Guide - Step by Step

**Get all required API keys for the MCP Research Agent**

---

## 🔑 Required API Keys

### 1. Anthropic API Key (REQUIRED)
**Cost**: Pay-as-you-go (~$0.30 per research)  
**Time**: 5 minutes

#### Steps:
1. Go to: https://console.anthropic.com/
2. Click "Sign Up" or "Log In"
3. Complete email verification
4. Navigate to "API Keys" in left sidebar
5. Click "Create Key"
6. Name it: "MCP Research Agent"
7. Copy the key (starts with `sk-ant-`)
8. **Save it immediately** - you won't see it again!

#### Add to .env:
```bash
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

---

### 2. Brave Search API Key (REQUIRED)
**Cost**: FREE (2,000 queries/month)  
**Time**: 10 minutes

#### Steps:
1. Go to: https://brave.com/search/api/
2. Click "Get Started" or "Sign Up"
3. Create account with email
4. Verify email
5. Log in to dashboard: https://api.search.brave.com/app/dashboard
6. Click "Add API Key" or "Create Key"
7. Name it: "MCP Research Agent"
8. Copy the key (starts with `BSA`)

#### Add to .env:
```bash
BRAVE_API_KEY=BSA_your-actual-key-here
```

---

### 3. LangSmith API Key (OPTIONAL - Recommended)
**Cost**: FREE tier available  
**Time**: 5 minutes

#### Steps:
1. Go to: https://smith.langchain.com/
2. Click "Sign Up with GitHub" (easiest)
3. Authorize LangSmith
4. Create new organization (if prompted)
5. Create new project: "mcp-research-agent"
6. Go to Settings (gear icon) → API Keys
7. Click "Create API Key"
8. Name it: "MCP Research Agent"
9. Copy the key (starts with `lsv2_`)

#### Add to .env:
```bash
LANGSMITH_API_KEY=lsv2_your-actual-key-here
LANGSMITH_PROJECT=mcp-research-agent
```

**Note**: If you skip LangSmith, comment out these lines in .env

---

## ✅ Verification Checklist

After getting keys, verify your `.env` file has:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...  # ✓ Starts with sk-ant-
BRAVE_API_KEY=BSA_...         # ✓ Starts with BSA

# Optional but recommended
LANGSMITH_API_KEY=lsv2_...    # ✓ Starts with lsv2_
LANGSMITH_PROJECT=mcp-research-agent
```

---

## 🧪 Test Your Keys

After adding keys to `.env`, test them:

### Test Anthropic:
```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 10,
    "messages": [{"role": "user", "content": "Hi"}]
  }'
```

Expected: JSON response with "content" field

### Test Brave Search:
```bash
curl "https://api.search.brave.com/res/v1/web/search?q=test" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"
```

Expected: JSON response with search results

---

## 🚨 Common Issues

### "Invalid API key"
- Check for extra spaces in .env
- Ensure no quotes around the key
- Verify key is active in dashboard

### "Rate limit exceeded"
- Anthropic: Check your tier at console.anthropic.com
- Brave: Free tier is 2000/month, check usage

### "Key not found"
- Ensure .env file is in project root
- Restart terminal to reload environment

---

## 💰 Cost Estimates

### Development (100 test researches)
- Anthropic: ~$30
- Brave Search: FREE
- LangSmith: FREE
- **Total**: ~$30

### Production (1000 researches/month)
- Anthropic: ~$300
- Brave Search: FREE (up to 2000) or $5/month (up to 15,000)
- LangSmith: FREE (up to 5000 traces)
- **Total**: ~$300-305/month

---

## 🔐 Security Best Practices

1. **Never commit .env to git** (already in .gitignore)
2. **Rotate keys periodically** (every 90 days)
3. **Use separate keys for dev/prod**
4. **Monitor usage** to detect unauthorized use
5. **Set spending limits** in Anthropic dashboard

---

## 📝 Next Steps

After getting all keys:
1. ✅ Add them to `.env`
2. ✅ Test connectivity (optional)
3. ➡️ Proceed to Gmail MCP setup
4. ➡️ Install dependencies

---

**Estimated Time**: 15-20 minutes total
