# Railway Deployment Fix - Monorepo Configuration

## The Problem
Railway is trying to build from the root directory, but this is a monorepo with separate backend and frontend services.

## The Solution
Deploy TWO separate services, each with its own root directory.

## Step-by-Step Fix

### 1. Delete Current Failed Deployment
1. Go to Railway dashboard
2. Find the failed MCPAIResearchAgent deployment
3. Delete it completely

### 2. Create Backend Service

1. Click **"New"** → **"GitHub Repo"**
2. Select: `bluedares/MCPAIResearchAgent`
3. **IMPORTANT**: Click **"Add variables"** or **"Configure"** BEFORE deploying
4. Set **Root Directory**: `/backend`
5. Add these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
   - **Watch Paths**: `/backend/**`

6. Add Environment Variables:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   TAVILY_API_KEY=tvly-your-key-here
   LANGSMITH_API_KEY=lsv2_pt_your-key-here
   LANGSMITH_PROJECT=mcp-research-agent
   LANGSMITH_TRACING_V2=true
   ENVIRONMENT=production
   DEBUG=false
   PORT=8000
   ```

7. Click **"Deploy"**

### 3. Create Frontend Service

1. In the SAME project, click **"New Service"** → **"GitHub Repo"**
2. Select: `bluedares/MCPAIResearchAgent` (same repo)
3. Set **Root Directory**: `/frontend`
4. Add these settings:
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm run preview -- --host 0.0.0.0 --port $PORT`
   - **Watch Paths**: `/frontend/**`

5. Add Environment Variables:
   ```
   VITE_API_URL=https://your-backend-service.up.railway.app
   ```
   (Replace with your actual backend URL from step 2)

6. Click **"Deploy"**

### 4. Update CORS in Backend

Once frontend is deployed, add frontend URL to backend environment variables:
```
CORS_ORIGINS=https://your-frontend-service.up.railway.app
```

## Alternative: Use Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Deploy backend
cd backend
railway up --service backend

# Deploy frontend
cd ../frontend
railway up --service frontend
```

## Why Root Deployment Failed

Railway's Nixpacks couldn't detect what to build because:
- Root directory has both Python (backend) and Node (frontend) code
- No clear entry point at root level
- Monorepo structure requires explicit service configuration

## Verification

After deployment:
1. Backend should be accessible at: `https://backend-production-xxxx.up.railway.app/health`
2. Frontend should be accessible at: `https://frontend-production-xxxx.up.railway.app`
3. Check logs for any errors

## Cost Estimate

- Backend: ~$3-5/month
- Frontend: ~$2-3/month
- Total: ~$5-8/month (within free tier if low traffic)

## Troubleshooting

**If backend fails:**
- Check all environment variables are set
- Verify Python version compatibility
- Check logs for missing dependencies

**If frontend fails:**
- Ensure `VITE_API_URL` points to correct backend URL
- Verify build completes successfully
- Check preview command works locally

**If services can't communicate:**
- Update CORS_ORIGINS in backend
- Verify VITE_API_URL in frontend
- Check network settings in Railway
