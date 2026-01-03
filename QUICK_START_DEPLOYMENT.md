# 🚀 AGENTIC AI - DEPLOYMENT CHECKLIST

## ✅ Pre-Deployment (Right Now)

- [ ] Hugging Face account created (huggingface.co)
- [ ] GitHub repo with `agentic-backend` available
- [ ] API Keys ready:
  - [ ] GROQ_API_KEY (get from console.groq.com)
  - [ ] OPENWEATHER_API_KEY (get from openweathermap.org)
  - [ ] OPENAI_API_KEY (optional, openai.com)

---

## 🎬 Part 1: Deploy Frontend to HF Spaces (5 min)

### 1.1 Create Space
```
Go to: https://huggingface.co/spaces
Click: Create new Space
  Name: agentic-ai-frontend
  Type: Docker
  Visibility: Public
Click: Create Space
```

### 1.2 Clone & Push
```powershell
$HF_USERNAME = "your-hf-username"
$HF_SPACE = "agentic-ai-frontend"

git clone https://huggingface.co/spaces/$HF_USERNAME/$HF_SPACE
cd $HF_SPACE

# Copy files from your agentic-backend directory
Copy-Item ..\app.py .
Copy-Item ..\requirements-hf.txt requirements.txt
Copy-Item ..\Dockerfile.hf Dockerfile
Copy-Item -Recurse ..\frontend\templates templates\
Copy-Item -Recurse ..\frontend\static static\

git add .
git commit -m "Initial: Agentic AI Frontend"
git push
```

**Wait 3–5 minutes for auto-build. Check status on HF Space page.**

### ✅ After Push
- Frontend URL: `https://{username}-agentic-ai-frontend.hf.space` (BOOKMARK THIS)
- Status should show: "Running" (green)
- If build fails: Check **Logs** tab on space page

---

## 🔧 Part 2: Deploy Backend to Railway (10 min)

### 2.1 Create Railway Project
```
Go to: https://railway.app
Sign up/Log in
Click: New Project
Select: Deploy from GitHub repo (agentic-backend)
Click: Deploy
```

### 2.2 Add PostgreSQL Service
```
In Railway Dashboard:
Click: Your Project
Click: Add Service → PostgreSQL
Railway auto-creates database
```

### 2.3 Set Start Command for Backend Service
```
Click: Backend service
Settings tab
Find: "Start Command"
Set to: uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### 2.4 Add Environment Variables
```
Click: Backend service
Variables tab
Add each:
  GROQ_API_KEY = your_groq_key_here
  OPENWEATHER_API_KEY = your_weather_key_here
  OPENAI_API_KEY = your_openai_key (optional)
  DEBUG = False
  LOG_LEVEL = INFO

(DATABASE_URL and SYNC_DATABASE_URL auto-filled by PostgreSQL)
```

### 2.5 Deploy & Get URL
```
Click: Deploy button
Wait 2–3 minutes
Find: "Public Domain" or "Domains" section
Copy: https://your-backend-xxxx.railway.app (BOOKMARK THIS)
```

### ✅ After Deploy
```powershell
# Test backend is working
curl https://your-backend-xxxx.railway.app/api/health

# Should return (takes ~5 sec first time):
# {"status": "healthy", "database": "connected", "timestamp": "..."}
```

---

## 🔗 Part 3: Connect Frontend to Backend (2 min)

### 3.1 Add Backend URL to HF Space Secrets
```
Go to: Your HF Space page
Click: Settings
Click: Repository secrets
Click: New secret
  Key: BACKEND_URL
  Value: https://your-backend-xxxx.railway.app
Click: Add secret
```

### 3.2 HF Space Auto-Redeploys
- Wait 1–2 minutes
- Your space will rebuild with the backend URL

---

## 🧪 Part 4: Test Full Stack

### 4.1 Open Frontend
```
Go to: https://{username}-agentic-ai-frontend.hf.space
```

### 4.2 Check Backend Status
- Look for small indicator (🟢 green = connected)
- If red, check BACKEND_URL in secrets

### 4.3 Test Features
- [ ] Chat: "What is the weather in London?"
- [ ] Upload: Click "📄" and upload a PDF/TXT
- [ ] Meetings: Click "➕" Schedule and create a meeting
- [ ] Meetings List: Click "📅" to see meetings

---

## 📊 Final Architecture

```
┌─────────────────────────────────────────┐
│  HF Spaces Frontend                     │
│  https://yourusername-agentic-ai...    │
│  (Port 7860, Auto-hosted)              │
└──────────────┬──────────────────────────┘
               │ (via BACKEND_URL secret)
               ↓
┌─────────────────────────────────────────┐
│  Railway Backend                        │
│  https://your-backend-xxxx.railway.app │
│  (Port 8000, Auto-hosted)              │
│                                         │
│  ├─ FastAPI app                        │
│  ├─ LangGraph agents                   │
│  └─ Groq LLM calls                     │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│  Railway PostgreSQL                     │
│  (Auto-provisioned)                     │
│                                         │
│  ├─ Meetings table                      │
│  ├─ Document metadata                   │
│  └─ Agent logs                          │
└─────────────────────────────────────────┘
```

---

## 💰 Cost
- **HF Spaces:** FREE forever
- **Railway:** FREE tier (~$5/month after)
- **Total:** $0 to start, ~$5/month at scale

---

## 🆘 Troubleshooting

| Issue | Fix |
|-------|-----|
| "Backend offline" | Check BACKEND_URL in HF Spaces secrets (copy exactly) |
| Backend build fails | Check Railway **Deployments** tab for logs |
| Upload fails | File too large (max 50MB) or unsupported format (use PDF/TXT) |
| Chat times out | Backend might be sleeping on free tier; refresh page |
| Can't find API keys | Get GROQ at console.groq.com, Weather at openweathermap.org |

---

## 📝 Next Steps

1. **Now:** Copy-paste Part 1 commands above
2. **Then:** Create Railway project (Part 2)
3. **Then:** Add BACKEND_URL secret (Part 3)
4. **Finally:** Test (Part 4)

**Total time: ~20 minutes, FREE deployment! 🚀**

---

## 📚 Reference Docs
- [SETUP_HF_SPACES.md](SETUP_HF_SPACES.md) – Detailed frontend guide
- [DEPLOY_BACKEND.md](DEPLOY_BACKEND.md) – Detailed backend guide
- [HF_SPACES_DEPLOYMENT.md](HF_SPACES_DEPLOYMENT.md) – Full architecture
