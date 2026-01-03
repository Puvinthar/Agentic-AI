# Backend Deployment on Railway or Render

## Railway.app (Recommended - Easiest)

### Step 1: Sign Up & Connect GitHub
1. Go to [railway.app](https://railway.app)
2. Sign up (free)
3. Click "New Project"
4. Select "Deploy from GitHub"
5. Select your `agentic-backend` repo
6. Click "Deploy"

### Step 2: Add PostgreSQL
1. In Railway dashboard, click your project
2. Click "Add Service"
3. Select "PostgreSQL"
4. Railway auto-provisions database with URL

### Step 3: Set Environment Variables
1. Click your Backend service
2. Click "Variables"
3. Add:
   ```
   GROQ_API_KEY=your_groq_key
   OPENWEATHER_API_KEY=your_weather_key
   OPENAI_API_KEY=your_openai_key (optional)
   DEBUG=False
   LOG_LEVEL=INFO
   ```

Railway auto-fills DATABASE_URL and SYNC_DATABASE_URL from the PostgreSQL service.

### Step 4: Set Start Command
1. Click "Settings"
2. Find "Start Command"
3. Set to:
   ```
   uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```

### Step 5: Deploy
1. Click "Deploy"
2. Wait 2–3 minutes
3. Check "Deployments" tab for status
4. Get public URL from "Public Domain" section (e.g., `https://agentic-backend-prod.railway.app`)

### Step 6: Link to HF Spaces
In your HF Space settings:
- Add secret: `BACKEND_URL=https://agentic-backend-prod.railway.app`
- Space auto-redeploys

---

## Render.com (Alternative)

### Step 1: Sign Up & Create Service
1. Go to [render.com](https://render.com)
2. Sign up (free)
3. Click "New" → "Web Service"
4. Connect your GitHub repo
5. Select `agentic-backend` repo

### Step 2: Configure
- **Name:** `agentic-backend`
- **Environment:** `Python 3`
- **Build Command:**
  ```
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```
  uvicorn backend.main:app --host 0.0.0.0 --port 8000
  ```
- **Plan:** Free tier

### Step 3: Add PostgreSQL
1. In Render dashboard, click "New" → "PostgreSQL"
2. Link it to your Web Service (auto-fills DATABASE_URL)

### Step 4: Environment Variables
Add in "Environment" tab:
```
GROQ_API_KEY=your_key
OPENWEATHER_API_KEY=your_key
OPENAI_API_KEY=optional
DEBUG=False
LOG_LEVEL=INFO
```

### Step 5: Deploy
1. Click "Create Web Service"
2. Wait 5–10 minutes for first deploy
3. Get URL from "Routes" section

### Step 6: Link to HF Spaces
In your HF Space settings:
- Add secret: `BACKEND_URL=https://your-service.onrender.com`
- Space auto-redeploys

---

## Verify Backend is Running

```bash
# Test endpoint (replace URL with your backend)
curl https://your-backend.railway.app/api/health

# Should return:
# {
#   "status": "healthy",
#   "database": "connected",
#   "timestamp": "2026-01-03T..."
# }
```

---

## Cost Comparison

| Platform | Cost | Uptime | Features |
|----------|------|--------|----------|
| **Railway** | FREE up to $5/mo | 99.9% | Best DX, auto-deploys |
| **Render** | FREE (auto-sleep) | 99.5% | Auto-sleep after 15min idle |
| **AWS/Heroku** | $7+/month | 99.99% | More control, more cost |

---

## Next Steps

1. ✅ Deploy to Railway or Render
2. ✅ Get backend public URL
3. ✅ Add `BACKEND_URL` to HF Spaces secrets
4. ✅ Test chat, uploads, meetings

Done! 🚀
