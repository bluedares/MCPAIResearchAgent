# Deployment Guide

## Docker Configuration Review

### ✅ Issues Fixed

1. **Backend Dockerfile**
   - ✅ Multi-stage build for smaller image size
   - ✅ Non-root user for security
   - ✅ Dynamic PORT support (Railway/deployment compatible)
   - ✅ Environment variable handling
   - ✅ Proper health checks

2. **Frontend Dockerfile**
   - ✅ Production build with Nginx
   - ✅ Multi-stage build
   - ✅ Nginx configuration for SPA
   - ✅ API proxy configuration
   - ✅ Health check endpoint

3. **Docker Compose**
   - ✅ Separate dev and prod profiles
   - ✅ Proper service dependencies
   - ✅ Health checks for all services
   - ✅ Network isolation

4. **.dockerignore Files**
   - ✅ Created for both frontend and backend
   - ✅ Excludes unnecessary files from build context

### Port Configuration

**Development:**
- Frontend Dev: `5173` (Vite)
- Backend: `8000` (FastAPI)
- PostgreSQL: `5432`
- Redis: `6379`
- Gmail MCP: `3001`
- Search MCP: `3002`

**Production:**
- Frontend: `80` (Nginx)
- Backend: `${PORT}` (Dynamic, defaults to 8000)
- Other services: Same as dev

### Running Locally

**Development Mode:**
```bash
# Start all services in dev mode
docker-compose --profile dev up

# Or start specific services
docker-compose up postgres redis backend frontend-dev
```

**Production Mode:**
```bash
# Start all services in prod mode
docker-compose --profile prod up

# Build and start
docker-compose --profile prod up --build
```

### Deployment Platforms

#### Railway Deployment

**Backend:**
```bash
# Railway will automatically detect Dockerfile
# Set environment variables in Railway dashboard:
- ANTHROPIC_API_KEY
- BRAVE_API_KEY
- LANGSMITH_API_KEY
- DATABASE_URL (Railway provides PostgreSQL)
- REDIS_URL (Railway provides Redis)
```

**Frontend:**
```bash
# Deploy using Dockerfile
# Railway will use PORT environment variable
```

#### Render Deployment

**Backend:**
```yaml
# render.yaml
services:
  - type: web
    name: mcp-research-backend
    env: docker
    dockerfilePath: ./backend/Dockerfile
    envVars:
      - key: PORT
        sync: false
      - key: ANTHROPIC_API_KEY
        sync: false
      - key: DATABASE_URL
        fromDatabase:
          name: research-db
          property: connectionString
```

**Frontend:**
```yaml
  - type: web
    name: mcp-research-frontend
    env: docker
    dockerfilePath: ./frontend/Dockerfile
```

### Environment Variables

**Required for Backend:**
```env
# API Keys
ANTHROPIC_API_KEY=your_key_here
BRAVE_API_KEY=your_key_here
LANGSMITH_API_KEY=your_key_here

# Database (provided by platform or use local)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Redis (optional, provided by platform)
REDIS_URL=redis://host:6379

# MCP Servers (if using)
GMAIL_MCP_URL=http://gmail-mcp:3001
SEARCH_MCP_URL=http://search-mcp:3002

# App Config
ENVIRONMENT=production
DEBUG=false
MAX_SUB_QUERIES=5
MAX_RETRY_ATTEMPTS=2
CORS_ORIGINS=https://your-frontend-domain.com
```

**Required for Frontend:**
```env
# API URL (set to your backend URL)
VITE_API_URL=https://your-backend-domain.com
```

### Health Checks

All services include health checks:

**Backend:** `GET /health`
**Frontend:** `GET /health`
**PostgreSQL:** `pg_isready`
**Redis:** `redis-cli ping`

### Security Best Practices

1. ✅ Non-root user in containers
2. ✅ Multi-stage builds (smaller attack surface)
3. ✅ Environment variable injection (no secrets in images)
4. ✅ Health checks for monitoring
5. ✅ Proper CORS configuration
6. ✅ Security headers in Nginx

### Troubleshooting

**Port Issues:**
- Backend uses `${PORT}` environment variable
- Railway/Render automatically set PORT
- Default fallback is 8000

**Build Issues:**
- Check .dockerignore files
- Ensure requirements.txt/package.json are present
- Verify Docker version (>= 20.10)

**Runtime Issues:**
- Check logs: `docker-compose logs -f service_name`
- Verify environment variables are set
- Check health endpoints
- Ensure database migrations ran

### Next Steps

1. Test locally with docker-compose
2. Set up deployment platform account
3. Configure environment variables
4. Deploy backend first
5. Deploy frontend with backend URL
6. Test end-to-end
7. Set up monitoring and alerts
