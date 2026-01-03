# 🎯 DEPLOYMENT CHECKLIST & COMMANDS

## 📋 BEFORE YOU START

### Get Your API Keys First
- [ ] GROQ_API_KEY (from console.groq.com)
- [ ] OPENWEATHER_API_KEY (from openweathermap.org)

**Read:** [GET_API_KEYS.md](GET_API_KEYS.md) for detailed instructions

---

## 🎬 STEP-BY-STEP DEPLOYMENT

### ✅ PART 1: FRONTEND TO HF SPACES (5 min)

**1.1 Create Space on Hugging Face**
```
URL: https://huggingface.co/spaces
Click: Create new Space
Name: agentic-ai-frontend
Type: Docker (NOT Gradio)
Visibility: Public
Click: Create Space
```
**Save your Space URL:** `https://huggingface.co/spaces/YOUR_USERNAME/agentic-ai-frontend`

---

**1.2 Clone Space & Copy Files**

Open **PowerShell** and run:

```powershell
# Configure
$HF_USERNAME = "YOUR-HF-USERNAME"
$HF_SPACE = "agentic-ai-frontend"

# Navigate to Desktop
cd Desktop

# Clone your space
git clone https://huggingface.co/spaces/$HF_USERNAME/$HF_SPACE
cd $HF_SPACE

# Copy files from backend
Copy-Item "D:\agentic-backend\app.py" .
Copy-Item "D:\agentic-backend\requirements-hf.txt" requirements.txt
Copy-Item "D:\agentic-backend\Dockerfile.hf" Dockerfile
Copy-Item -Recurse "D:\agentic-backend\frontend\templates" .
Copy-Item -Recurse "D:\agentic-backend\frontend\static" .

# Verify files exist
ls

# Add git ignore
@"
__pycache__/
*.pyc
*.pyo
.env
.env.local
uploads/
.DS_Store
*.egg-info/
"@ | Out-File -Encoding UTF8 .gitignore

# Commit and push
git config --global user.email "your-email@gmail.com"
git config --global user.name "Your Name"
git add .
git status
git commit -m "Initial commit: Agentic AI Frontend"
git push
```

**When asked for password:** Use your HF token (get from https://huggingface.co/settings/tokens)

**1.3 Wait for Build**
```
Go to: https://huggingface.co/spaces/YOUR_USERNAME/agentic-ai-frontend
Wait 3-5 minutes for status to show: Running ✅
```

**Save your Frontend URL:** `https://YOUR_USERNAME-agentic-ai-frontend.hf.space`

---

### ✅ PART 2: BACKEND TO RAILWAY (10 min)

**2.1 Create Railway Project**
```
URL: https://railway.app
Sign up/login
New Project
Deploy from GitHub repo (select: agentic-backend)
Click: Deploy
```

**2.2 Add PostgreSQL**
```
In Railway Dashboard:
Click: Your Project
Add Service → PostgreSQL
(Railway auto-creates database)
```

**2.3 Set Start Command**
```
Click: Backend service
Settings tab
Start Command: uvicorn backend.main:app --host 0.0.0.0 --port 8000
Save
```

**2.4 Add Environment Variables**

```
Click: Backend service
Variables tab
Add each (click + each time):

1. GROQ_API_KEY = your-groq-key
2. OPENWEATHER_API_KEY = your-weather-key
3. OPENAI_API_KEY = your-openai-key (optional)
4. DEBUG = False
5. LOG_LEVEL = INFO

(DATABASE_URL auto-filled by PostgreSQL)
```

**2.5 Deploy & Get URL**
```
Railway auto-deploys
Wait 2-3 minutes for status: Running ✅
Find: Domains section
Copy: https://your-backend-xxxx.railway.app
```

**2.6 Test Backend**
```powershell
$BACKEND = "https://your-backend-xxxx.railway.app"
curl "$BACKEND/api/health"

# Should return: {"status": "healthy", "database": "connected", ...}
```

**Save your Backend URL:** `https://your-backend-xxxx.railway.app`

---

### ✅ PART 3: CONNECT THEM (2 min)

**3.1 Add Backend URL to HF Space Secrets**
```
Go to: https://huggingface.co/spaces/YOUR_USERNAME/agentic-ai-frontend
Click: Settings
Click: Repository secrets
Click: New secret

Secret name: BACKEND_URL
Secret value: https://your-backend-xxxx.railway.app
(Copy from Part 2.5)

Click: Add secret
```

**3.2 Wait for Auto-Redeploy**
```
Go to your HF Space
Wait 1-2 minutes
Status should show: Running ✅
```

---

### ✅ PART 4: TEST (5 min)

**4.1 Open Your App**
```
Go to: https://YOUR_USERNAME-agentic-ai-frontend.hf.space
```

**4.2 Check Backend Status**
```
Bottom left corner should show: 🟢 Backend online
If red, check BACKEND_URL in HF Spaces secrets
```

**4.3 Test Weather**
```
Type in chat: "What is the weather in London?"
Press Enter
Should get weather response
```

**4.4 Test Upload**
```
Click: 📄 Upload button
Select any PDF or TXT file
Should see: ✅ File uploaded
```

**4.5 Test Meetings**
```
Click: ➕ Schedule button
Fill in:
  Title: Team Meeting
  Date: Tomorrow
  Time: 10:00 AM
  Location: Conference Room
Click: Create Meeting
Should see: ✅ Meeting created
```

---

## 📊 FINAL URLS TO BOOKMARK

```
Frontend (HF Spaces):  https://YOUR_USERNAME-agentic-ai-frontend.hf.space
Backend (Railway):     https://your-backend-xxxx.railway.app
API Docs:             https://your-backend-xxxx.railway.app/docs
```

---

## 🆘 IF SOMETHING GOES WRONG

### "Backend offline"
1. Check BACKEND_URL in HF Spaces secrets matches exactly
2. Remove trailing slash (/)
3. Test: `curl https://your-backend-url/api/health`

### Build fails on HF
1. Go to HF Space > Logs tab
2. Read error message
3. Fix and `git push` again

### Railway deployment fails
1. Go to Railway > Deployments tab
2. Read logs
3. Check all env variables are set correctly

### API key errors
1. Go to Railway > Backend service > Logs
2. Look for "Invalid API key" messages
3. Verify key in variables tab is correct

---

## 💰 COST

| Service | Cost |
|---------|------|
| HF Spaces (Frontend) | **FREE** ✅ |
| Railway (Backend + DB) | **FREE** (up to $5/mo) ✅ |
| **TOTAL** | **$0-5/month** ✅ |

---

## 🎓 USEFUL LINKS

- [Full Beginner Guide](DEPLOYMENT_BEGINNER_GUIDE.md) - Detailed with screenshots
- [Get API Keys](GET_API_KEYS.md) - How to get GROQ & Weather keys
- [HF Spaces Docs](https://huggingface.co/docs/hub/spaces-overview)
- [Railway Docs](https://docs.railway.app/)

---

## ✨ YOU'RE ALL SET!

**Ready to deploy?**
1. Read: [GET_API_KEYS.md](GET_API_KEYS.md) (get your keys)
2. Follow: [DEPLOYMENT_BEGINNER_GUIDE.md](DEPLOYMENT_BEGINNER_GUIDE.md) (step-by-step)
3. Bookmark: Your 3 URLs above
4. Test: The 5 tests in Part 4

**Good luck! 🚀**
