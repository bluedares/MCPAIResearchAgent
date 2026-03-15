# Railway Deployment Guide

## Quick Deploy to Railway

This project is configured for Railway deployment with separate frontend and backend services.

### Prerequisites
- Railway account (https://railway.app)
- GitHub repository connected to Railway

### Deployment Steps

#### 1. Create New Project on Railway
```bash
# Option A: Deploy from GitHub (Recommended)
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose: bluedares/MCPAIResearchAgent
5. Railway will detect the monorepo structure

# Option B: Deploy via Railway CLI
railway login
railway init
railway up
```

#### 2. Create Two Services

**Service 1: Backend**
- Root Directory: `/backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
- Health Check: `/health`

**Service 2: Frontend**
- Root Directory: `/frontend`
- Build Command: `npm install && npm run build`
- Start Command: `npm run preview -- --host 0.0.0.0 --port $PORT`

#### 3. Set Environment Variables

**Backend Service Variables:**
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
TAVILY_API_KEY=tvly-your-key-here
LANGSMITH_API_KEY=lsv2_pt_your-key-here
LANGSMITH_PROJECT=mcp-research-agent
LANGSMITH_TRACING_V2=true
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=https://your-frontend.railway.app
```

**Frontend Service Variables:**
```bash
VITE_API_URL=https://your-backend.railway.app
```

#### 4. Add PostgreSQL and Redis (Optional)

**Add PostgreSQL:**
1. Click "New" → "Database" → "Add PostgreSQL"
2. Railway will auto-populate `DATABASE_URL` in backend service

**Add Redis:**
1. Click "New" → "Database" → "Add Redis"
2. Railway will auto-populate `REDIS_URL` in backend service

### Service Configuration Files

The project includes Railway configuration files:

- `railway.json` - Root project configuration
- `backend/railway.toml` - Backend service configuration
- `frontend/railway.toml` - Frontend service configuration

### Deployment Architecture

```
Railway Project: MCPAIResearchAgent
├── Backend Service (Python/FastAPI)
│   ├── Port: Auto-assigned by Railway
│   ├── Domain: backend-production-xxxx.up.railway.app
│   └── Health Check: /health
│
├── Frontend Service (React/Vite)
│   ├── Port: Auto-assigned by Railway
│   ├── Domain: frontend-production-xxxx.up.railway.app
│   └── Environment: VITE_API_URL points to backend
│
├── PostgreSQL Database (Optional)
│   └── Auto-connected to backend
│
└── Redis Cache (Optional)
    └── Auto-connected to backend
```

### Cost Estimation

**Railway Free Tier:**
- $5/month in credits
- ~500 execution hours

**Estimated Monthly Cost:**
- Backend: $3-5/month (low traffic)
- Frontend: $2-3/month (static serving)
- PostgreSQL: $5/month (if using Railway's DB)
- Redis: $5/month (if using Railway's Redis)

**Total: $10-18/month** (or use external free-tier databases)

### Cost Optimization Tips

1. **Use Free Database Alternatives:**
   - Neon (PostgreSQL): Free tier with 0.5GB storage
   - Upstash (Redis): Free tier with 10K commands/day

2. **Set Sleep Policy:**
   - Configure services to sleep after inactivity
   - Reduces execution hours

3. **Optimize Build Times:**
   - Use Docker layer caching
   - Minimize dependencies

### Troubleshooting

**Build Fails:**
- Check `railway.toml` configuration
- Verify root directory is set correctly
- Check build logs for missing dependencies

**Backend Won't Start:**
- Verify all environment variables are set
- Check health check endpoint is responding
- Review application logs

**Frontend Can't Connect to Backend:**
- Verify `VITE_API_URL` points to backend domain
- Check CORS settings in backend
- Ensure backend is deployed and running

**Database Connection Issues:**
- Verify `DATABASE_URL` is set
- Check database service is running
- Review connection string format

### Monitoring

**View Logs:**
```bash
railway logs
```

**Check Metrics:**
- CPU usage
- Memory usage
- Request count
- Response times

### Updating Deployment

**Via Git Push:**
```bash
git add .
git commit -m "Update deployment"
git push origin main
# Railway auto-deploys on push
```

**Via Railway CLI:**
```bash
railway up
```

### Custom Domains (Optional)

1. Go to service settings
2. Click "Generate Domain" or "Custom Domain"
3. Add your domain
4. Update DNS records

### Rollback

```bash
# Via Railway Dashboard
1. Go to Deployments
2. Find previous successful deployment
3. Click "Redeploy"

# Via Railway CLI
railway rollback
```

## Alternative: Docker Deployment

If you prefer Docker-based deployment:

```bash
# Railway will auto-detect Dockerfile
# Make sure Dockerfile is in service root directory
```

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Project Issues: https://github.com/bluedares/MCPAIResearchAgent/issues
