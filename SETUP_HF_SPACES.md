# Quick HF Spaces Setup Guide (PowerShell)

## Prerequisites
- Hugging Face account (free at huggingface.co)
- Git installed
- This repo cloned locally

## 1️⃣ Create HF Space (5 min)

```powershell
# Go to https://huggingface.co/spaces
# Click "Create new Space"
# - Name: agentic-ai-frontend (or your choice)
# - Type: Docker
# Click "Create Space"
```

Note your space URL: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`

## 2️⃣ Clone Space Repo

```powershell
$HF_USERNAME = "your-username"
$HF_SPACE_NAME = "agentic-ai-frontend"

git clone https://huggingface.co/spaces/$HF_USERNAME/$HF_SPACE_NAME
cd $HF_SPACE_NAME
```

## 3️⃣ Copy Frontend Files

```powershell
# From your agentic-backend directory, copy:
Copy-Item ..\app.py .
Copy-Item ..\requirements-hf.txt requirements.txt
Copy-Item ..\Dockerfile.hf Dockerfile
Copy-Item -Recurse ..\frontend\templates templates\
Copy-Item -Recurse ..\frontend\static static\
```

Your HF Space folder should now look like:
```
├── Dockerfile
├── requirements.txt
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── .git/
```

## 4️⃣ Commit & Push

```powershell
git add .
git commit -m "Initial commit: Agentic AI Frontend"
git push
```

HF Spaces will auto-detect the Dockerfile and start building. Wait 3–5 minutes.

## 5️⃣ Check Deployment Status

Visit your space: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`

Look for:
- **Build status** at the top (should say "Running" with green checkmark)
- **App preview** on the right side
- **Logs** tab to debug if needed

## 6️⃣ Set Backend URL

Your frontend is now live, but it needs a backend! Options:

### Option A: Railway (Recommended - Free tier)
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repo (`agentic-backend`)
3. Add environment variables:
   ```
   GROQ_API_KEY=your_key
   OPENWEATHER_API_KEY=your_key
   DATABASE_URL=postgresql+asyncpg://...
   SYNC_DATABASE_URL=postgresql://...
   ```
4. Railway auto-deploys → you get a public URL like `https://agentic-backend-prod.railway.app`

### Option B: Render (Free tier)
1. Go to [render.com](https://render.com)
2. New Web Service from GitHub
3. Set build: `pip install -r requirements.txt`
4. Set start: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`
5. Add env vars, deploy

### Option C: ngrok (Localhost, Dev Only)
```powershell
# In your local agentic-backend folder
pip install ngrok
python -m uvicorn backend.main:app --port 8000

# In another terminal
ngrok http 8000
# Get URL like: https://abc123.ngrok.io
```

## 7️⃣ Connect Frontend to Backend

Once backend is running:

1. Go to your HF Space page
2. Click **Settings** → **Repository secrets**
3. Add a secret:
   - Key: `BACKEND_URL`
   - Value: `https://your-backend-url.com` (or `https://abc123.ngrok.io` for ngrok)
4. Click Add secret
5. Space auto-redeploys

## 8️⃣ Test

Open your HF Space URL and:
- Check backend status (should show green)
- Send a chat message
- Upload a document
- Create a meeting

---

## Cost

| Component | Cost |
|-----------|------|
| HF Spaces Frontend | **FREE** |
| Railway Backend (free tier) | FREE (up to $5/month) |
| **Total** | **FREE** |

---

## Troubleshooting

**"Backend offline" message?**
- Double-check BACKEND_URL in HF Space secrets (no trailing slash)
- Verify backend service is actually running
- Check backend logs on Railway/Render

**"Failed to upload file"?**
- File size too large (max 50MB)
- Unsupported format (use PDF, TXT, DOC, DOCX)

**Space build failed?**
- Check **Logs** tab on your space page
- Make sure Dockerfile exists
- Verify requirements.txt is correct

**Need to update?**
```powershell
git add .
git commit -m "Your update message"
git push
# HF auto-rebuilds in 3–5 minutes
```

---

## Next Steps

✅ HF Spaces frontend deployed  
⏳ Deploy backend (Railway/Render)  
⏳ Add BACKEND_URL to HF Spaces secrets  
⏳ Test full stack  

Good luck! 🚀
