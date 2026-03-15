# DEVELOPMENT SETUP - Quick Start Guide

**Get the MCP Research Agent running locally in under 30 minutes**

---

## ⚡ Prerequisites

Before starting, ensure you have:

| Requirement | Version | Check Command | Install Link |
|-------------|---------|---------------|--------------|
| **Python** | 3.12+ | `python --version` | [python.org](https://www.python.org/downloads/) |
| **Node.js** | 18+ | `node --version` | [nodejs.org](https://nodejs.org/) |
| **npm** | 9+ | `npm --version` | Included with Node.js |
| **Git** | Any | `git --version` | [git-scm.com](https://git-scm.com/) |
| **Google Account** | - | - | For Gmail MCP |

**Optional**:
- Docker Desktop (for containerized development)
- VS Code with Python + TypeScript extensions

---

## 🚀 Step-by-Step Setup

### Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd MCPAIResearchAgent
```

---

### Step 2: API Keys Setup

#### 2.1 Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to "API Keys"
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-`)

#### 2.2 Brave Search API Key

1. Go to [brave.com/search/api](https://brave.com/search/api/)
2. Sign up for free tier (2000 queries/month)
3. Create API key
4. Copy the key (starts with `BSA`)

#### 2.3 LangSmith API Key (Optional but Recommended)

1. Go to [smith.langchain.com](https://smith.langchain.com/)
2. Sign up with GitHub
3. Create new project: "mcp-research-agent"
4. Go to Settings → API Keys
5. Create key and copy

---

### Step 3: Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your favorite editor
nano .env  # or vim, code, etc.
```

**Update these values in `.env`**:
```bash
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
BRAVE_API_KEY=BSA_your-actual-key-here
LANGSMITH_API_KEY=lsv2_your-actual-key-here  # Optional
```

**Save and close** the file.

---

### Step 4: Gmail MCP Setup (Critical!)

This is the most time-consuming step (~30-45 minutes first time).

#### 4.1 Google Cloud Console Setup

1. **Go to [console.cloud.google.com](https://console.cloud.google.com/)**

2. **Create New Project**:
   - Click "Select a project" dropdown
   - Click "New Project"
   - Name: `MCP Research Agent`
   - Click "Create"
   - Wait for project creation (~30 seconds)

3. **Enable Gmail API**:
   - Ensure new project is selected
   - Go to "APIs & Services" → "Library"
   - Search: "Gmail API"
   - Click "Gmail API"
   - Click "Enable"

4. **Configure OAuth Consent Screen**:
   ```
   Navigation: APIs & Services → OAuth consent screen
   
   User Type: External
   Click "Create"
   
   App Information:
   - App name: MCP Research Agent
   - User support email: [your-email@gmail.com]
   - Developer contact: [your-email@gmail.com]
   Click "Save and Continue"
   
   Scopes:
   - Click "Add or Remove Scopes"
   - Search and add: "https://www.googleapis.com/auth/gmail.send"
   - (Optional) Add: "https://www.googleapis.com/auth/gmail.readonly"
   - Click "Update"
   - Click "Save and Continue"
   
   Test Users:
   - Click "Add Users"
   - Enter your Gmail address
   - Click "Add"
   - Click "Save and Continue"
   
   Summary:
   - Review and click "Back to Dashboard"
   ```

5. **Create OAuth Credentials**:
   ```
   Navigation: APIs & Services → Credentials
   
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "MCP Gmail Client"
   - Click "Create"
   - Click "Download JSON" (downloads as client_secret_xxx.json)
   - Click "OK"
   ```

#### 4.2 Setup Gmail MCP Locally

```bash
# Create Gmail MCP directory
mkdir -p mcp_servers/gmail
cd mcp_servers/gmail

# Move downloaded credentials
# (Adjust path to your Downloads folder)
mv ~/Downloads/client_secret_*.json credentials.json

# Verify file exists
ls -la credentials.json
```

#### 4.3 Run OAuth Flow

```bash
# This will open browser for authentication
npx -y @modelcontextprotocol/server-gmail
```

**What happens**:
1. Terminal shows: "Opening browser for authentication..."
2. Browser opens to Google OAuth page
3. Select your Google account
4. Click "Continue" (may show "Google hasn't verified this app" - click "Continue" anyway)
5. Review permissions and click "Allow"
6. Browser shows: "Authentication successful! You can close this window."
7. Terminal shows: "Authentication successful. Token saved."

**Verify token created**:
```bash
ls -la
# Should see:
# - credentials.json
# - token.json  ← This was just created
```

#### 4.4 Test Gmail MCP

```bash
# Test sending email to yourself
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"send_email","arguments":{"to":"your-email@gmail.com","subject":"MCP Test","body":"Hello from Gmail MCP!"}}}' | npx -y @modelcontextprotocol/server-gmail
```

**Expected output**: JSON response with email ID

**Check your Gmail**: You should receive the test email!

#### 4.5 Secure Credentials

```bash
# Return to project root
cd ../..

# Verify .gitignore includes these files
grep -E "credentials.json|token.json" .gitignore

# Should see:
# mcp_servers/gmail/credentials.json
# mcp_servers/gmail/token.json
```

**CRITICAL**: Never commit these files to git!

---

### Step 5: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import langchain, langgraph, anthropic; print('✅ All packages installed')"
```

**Expected output**: `✅ All packages installed`

---

### Step 6: Frontend Setup

```bash
# Navigate to frontend (from project root)
cd frontend

# Install dependencies
npm install

# Verify installation
npm list react vite tailwindcss
```

**Expected output**: Package tree showing installed versions

---

### Step 7: Initialize Shadcn/ui Components

```bash
# Still in frontend directory
npx shadcn-ui@latest init

# Answer prompts:
# - Would you like to use TypeScript? Yes
# - Which style would you like to use? Default
# - Which color would you like to use as base color? Slate
# - Where is your global CSS file? src/index.css
# - Would you like to use CSS variables for colors? Yes
# - Where is your tailwind.config.js located? tailwind.config.js
# - Configure the import alias for components? @/components
# - Configure the import alias for utils? @/lib/utils

# Install required components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add input
npx shadcn-ui@latest add textarea
npx shadcn-ui@latest add card
npx shadcn-ui@latest add progress
npx shadcn-ui@latest add alert
npx shadcn-ui@latest add badge
```

---

### Step 8: Database Initialization (Local SQLite)

```bash
# Return to backend
cd ../backend

# Ensure venv is activated
source venv/bin/activate

# Create database directory
mkdir -p data

# Database will be auto-created on first run
# For now, just verify the directory exists
ls -la data/
```

---

### Step 9: Run Backend

```bash
# From backend directory with venv activated
uvicorn api.main:app --reload --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Test backend**:
```bash
# In a new terminal
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

**Keep this terminal running!**

---

### Step 10: Run Frontend

```bash
# In a new terminal, navigate to frontend
cd frontend

# Start dev server
npm run dev
```

**Expected output**:
```
  VITE v5.4.8  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**Open browser**: http://localhost:5173

---

### Step 11: Test End-to-End Workflow

1. **Open UI**: http://localhost:5173

2. **Enter Research Topic**:
   ```
   Latest developments in quantum computing
   ```

3. **Enter Client Email**:
   ```
   your-email@gmail.com
   ```

4. **Click "Start Research"**

5. **Watch Progress**:
   - 🧠 Planning (5-10 seconds)
   - 🔍 Researching (10-20 seconds)
   - 📝 Summarizing (10-15 seconds)
   - ✅ Verifying (5-10 seconds)
   - 📧 Sending Email (2-5 seconds)

6. **Check Email**: You should receive research summary!

---

## 🐳 Docker Setup (Alternative)

If you prefer Docker:

```bash
# Build and run all services
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:5173
```

**Note**: Gmail MCP OAuth flow is trickier in Docker. Recommend local setup first.

---

## 🧪 Running Tests

### Backend Tests

```bash
cd backend
source venv/bin/activate
pytest tests/ -v --cov
```

### Frontend Tests

```bash
cd frontend
npm test
```

---

## 🔍 Verify LangSmith Integration (Optional)

If you configured LangSmith:

1. Run a research workflow
2. Go to [smith.langchain.com](https://smith.langchain.com/)
3. Navigate to your project: "mcp-research-agent"
4. Click "Traces"
5. You should see the workflow execution with all agent steps!

---

## 🚨 Troubleshooting

### Issue: "Python version mismatch"

```bash
# Check Python version
python --version

# If not 3.12+, install from python.org
# Or use pyenv:
pyenv install 3.12.0
pyenv local 3.12.0
```

### Issue: "Gmail OAuth token expired"

```bash
# Delete token and re-authenticate
rm mcp_servers/gmail/token.json
cd mcp_servers/gmail
npx -y @modelcontextprotocol/server-gmail
```

### Issue: "Module not found: langchain"

```bash
# Ensure venv is activated
source backend/venv/bin/activate

# Reinstall dependencies
pip install -r backend/requirements.txt --force-reinstall
```

### Issue: "BRAVE_API_KEY not found"

```bash
# Check .env file exists
cat .env | grep BRAVE_API_KEY

# If missing, add it:
echo "BRAVE_API_KEY=BSA_your_key_here" >> .env
```

### Issue: "Port 8000 already in use"

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
uvicorn api.main:app --reload --port 8001
```

### Issue: "npm install fails"

```bash
# Clear cache and retry
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### Issue: "Database locked"

```bash
# Stop all backend processes
pkill -f uvicorn

# Delete database and restart
rm backend/data/research_agent.db
```

---

## 📁 Project Structure Verification

After setup, your project should look like:

```
MCPAIResearchAgent/
├── .env                        ✅ Created
├── .gitignore                  ✅ Exists
├── README.md                   ✅ Exists
├── backend/
│   ├── venv/                   ✅ Created
│   ├── requirements.txt        ✅ Exists
│   ├── agents/                 📁 Empty (will create)
│   ├── graph/                  📁 Empty (will create)
│   ├── mcp_tools/              📁 Empty (will create)
│   └── api/                    📁 Empty (will create)
├── frontend/
│   ├── node_modules/           ✅ Created
│   ├── package.json            ✅ Exists
│   └── src/                    📁 Empty (will create)
├── mcp_servers/
│   └── gmail/
│       ├── credentials.json    ✅ Created (gitignored)
│       └── token.json          ✅ Created (gitignored)
└── docs/
    ├── PROJECT_CORE.md         ✅ Exists
    ├── MCP_INTEGRATION_GUIDE.md ✅ Exists
    └── TECH_STACK.md           ✅ Exists
```

---

## ✅ Setup Checklist

- [ ] Python 3.12+ installed
- [ ] Node.js 18+ installed
- [ ] Anthropic API key obtained
- [ ] Brave Search API key obtained
- [ ] LangSmith account created (optional)
- [ ] Google Cloud project created
- [ ] Gmail API enabled
- [ ] OAuth consent screen configured
- [ ] credentials.json downloaded
- [ ] Gmail OAuth flow completed (token.json created)
- [ ] .env file configured
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Shadcn/ui components added
- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:5173
- [ ] End-to-end test successful (email received)

---

## 🎯 Next Steps

Now that your environment is set up:

1. **Read Architecture Docs**: `docs/PROJECT_CORE.md`
2. **Understand MCP Integration**: `docs/MCP_INTEGRATION_GUIDE.md`
3. **Start Building Agents**: See `docs/AGENT_SPECIFICATIONS.md` (coming next)
4. **Implement LangGraph Workflow**: See `docs/LANGGRAPH_WORKFLOW.md` (coming next)

---

## 💡 Development Tips

### Hot Reload

Both backend and frontend support hot reload:
- **Backend**: Uvicorn auto-reloads on file changes
- **Frontend**: Vite HMR updates instantly

### Debugging

**Backend**:
```python
# Add breakpoints
import pdb; pdb.set_trace()

# Or use VS Code debugger
```

**Frontend**:
```typescript
// Use browser DevTools
console.log('Debug:', data);
debugger;
```

### LangSmith Traces

Every workflow execution is automatically traced if `LANGSMITH_API_KEY` is set. View at [smith.langchain.com](https://smith.langchain.com/).

### Cost Monitoring

Check Claude API usage at [console.anthropic.com](https://console.anthropic.com/) → Usage.

---

## 🆘 Getting Help

- **Documentation**: Check `docs/` folder
- **Issues**: GitHub Issues
- **MCP Docs**: [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- **LangGraph Docs**: [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/)

---

**Setup Time**: ~30-45 minutes (first time)  
**Subsequent Setups**: ~5 minutes

**Ready to build!** 🚀
