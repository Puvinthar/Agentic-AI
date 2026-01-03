# Hugging Face Spaces Deployment Guide

## Deploy Frontend to HF Spaces (Free)

### Step 1: Create HF Space
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Name it (e.g., `agentic-ai-frontend`)
4. Choose **Space type: Docker** (or Gradio if you want simpler)
5. Click **Create Space**

### Step 2: Clone & Push Frontend
```bash
# Clone your new space repo
git clone https://huggingface.co/spaces/<your-username>/<space-name>
cd <space-name>

# Copy files from your local agentic-backend
cp ../agentic-backend/app.py .
cp ../agentic-backend/requirements-hf.txt ./requirements.txt
cp -r ../agentic-backend/frontend/templates ./
cp -r ../agentic-backend/frontend/static ./
```

### Step 3: Create Dockerfile
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY frontend/ ./frontend/

EXPOSE 7860

CMD ["python", "app.py"]
```

### Step 4: Set Environment Variables
1. On HF Space page, click **Settings** → **Repository secrets**
2. Add secret: `BACKEND_URL` = your backend public URL
   - **Local testing:** `http://localhost:8000`
   - **Production:** `https://your-backend-domain.com` or `https://your-railway.app`

### Step 5: Push to HF Spaces
```bash
git add .
git commit -m "Initial commit - Agentic AI Frontend"
git push
```

HF will auto-build and deploy! Wait 3-5 minutes.

---

## Deploy Backend Separately (Required)

You have options:

### Option A: Railway (Easiest - Free tier)
1. Go to [railway.app](https://railway.app)
2. Import from GitHub (your agentic-backend repo)
3. Add environment variables (GROQ_API_KEY, OPENWEATHER_API_KEY, DATABASE_URL, etc.)
4. Deploy PostgreSQL plugin
5. Get public URL: `https://your-project.railway.app`
6. Add to HF Space secret: `BACKEND_URL=https://your-project.railway.app`

### Option B: Render (Free tier)
1. Go to [render.com](https://render.com)
2. Create new **Web Service** from GitHub
3. Set build command: `pip install -r requirements.txt`
4. Start command: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`
5. Add environment variables
6. Deploy

### Option C: Keep Running Locally (Dev Only)
- Run backend on your machine: `python -m uvicorn backend.main:app --port 8000`
- Use ngrok to expose: `ngrok http 8000` → Get public URL
- Add to HF Space secret: `BACKEND_URL=https://ngrok-url.ngrok.io`

---

## Architecture After Deployment

```
HF Spaces Frontend (5000)
    ↓
    └─→ Railway Backend (8000)
            ↓
            └─→ Railway PostgreSQL
```

---

## Verify Deployment

1. Open your HF Space URL: `https://<username>-<space-name>.hf.space`
2. Check backend status indicator (should show green)
3. Try a query
4. Upload a document
5. Create a meeting

---

## Troubleshooting

**"Backend offline" message?**
- Check BACKEND_URL in HF Space secrets
- Verify backend service is running
- Check CORS settings in backend/main.py (should allow *)

**Slow builds on HF Spaces?**
- Reduce dependencies in requirements.txt
- Use slim base images

**Need to update?**
```bash
git add .
git commit -m "Update message"
git push
# HF auto-redeploys in 3-5 minutes
```

---

## Cost

- **HF Spaces Frontend:** FREE (0 cost)
- **Railway Backend + DB:** FREE tier up to $5/month (~2K requests)
- **Total:** FREE or ~$5/month

After free tier exhausted, Railway costs ~$5-10/month for small projects.
