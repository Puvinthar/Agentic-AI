# Agentic AI Backend API

**Standalone FastAPI backend with Swagger documentation**

## 🌐 Live API Documentation

- **Swagger UI (Interactive):** [Your Deployment URL]/docs
- **ReDoc:** [Your Deployment URL]/redoc
- **OpenAPI JSON:** [Your Deployment URL]/openapi.json

## 🚀 Quick Deploy Options

### Option 1: Render.com (Recommended - Free Tier)

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** agentic-ai-backend
   - **Environment:** Docker
   - **Dockerfile Path:** backend-only/Dockerfile
   - **Plan:** Free
5. Add Environment Variables:
   - `DATABASE_URL`
   - `GROQ_API_KEY`
   - `OPENWEATHER_API_KEY`
6. Deploy!

**Result:** Your API will be at `https://agentic-ai-backend.onrender.com/docs`

---

### Option 2: Railway.app (Free $5 Credit)

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Configure:
   - **Root Directory:** Leave empty
   - **Start Command:** `python backend-only/app.py`
5. Add Environment Variables (same as above)
6. Deploy!

**Result:** Your API will be at `https://your-app.railway.app/docs`

---

### Option 3: Fly.io (Free Tier)

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Navigate to backend-only directory
cd backend-only

# Launch app
fly launch

# Set environment variables
fly secrets set DATABASE_URL="your_database_url"
fly secrets set GROQ_API_KEY="your_groq_key"
fly secrets set OPENWEATHER_API_KEY="your_weather_key"

# Deploy
fly deploy
```

**Result:** Your API will be at `https://your-app.fly.dev/docs`

---

### Option 4: Separate Hugging Face Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Create New Space:
   - **Name:** agentic-ai-backend-api
   - **SDK:** Docker
   - **Visibility:** Public
3. Clone the new space
4. Copy these files:
   ```bash
   cp backend-only/Dockerfile [space-directory]/
   cp backend-only/app.py [space-directory]/
   cp -r backend [space-directory]/
   cp requirements.txt [space-directory]/
   ```
5. Create `[space-directory]/README.md`:
   ```markdown
   ---
   title: Agentic AI Backend API
   emoji: 🤖
   colorFrom: purple
   colorTo: indigo
   sdk: docker
   app_port: 8000
   ---
   
   # Agentic AI Backend API
   
   Interactive API documentation available at `/docs`
   ```
6. Add secrets in Space Settings
7. Push and deploy!

**Result:** Your API will be at `https://huggingface.co/spaces/YOUR-USERNAME/agentic-ai-backend-api`

---

## 📡 API Endpoints

### Chat
```bash
POST /api/chat
Content-Type: application/json

{
  "query": "What is the weather in Chennai?"
}
```

### Upload Document
```bash
POST /api/upload
Content-Type: multipart/form-data

file: [your-file.pdf]
```

### Create Meeting
```bash
POST /api/meetings
Content-Type: application/json

{
  "title": "Team Meeting",
  "scheduled_date": "2026-01-05T10:00:00",
  "location": "Chennai"
}
```

### Query Meetings
```bash
GET /api/meetings?query=tomorrow
```

### Health Check
```bash
GET /api/health
```

---

## 🔧 Local Development

```bash
# From project root
cd backend-only
python app.py

# Access Swagger UI
open http://localhost:8000/docs
```

---

## 🌟 Why This Deployment?

- ✅ **Separate API Documentation** - Public Swagger UI
- ✅ **No Frontend Overhead** - Pure backend API
- ✅ **Easier Testing** - Interactive API explorer
- ✅ **Better Performance** - No frontend assets to serve
- ✅ **Parallel Deployment** - Doesn't affect main full-stack app

---

## 📞 Support

For issues with deployment, check:
1. Environment variables are set correctly
2. Database connection is accessible
3. API keys are valid
4. Port 8000 is exposed (most platforms auto-detect)
