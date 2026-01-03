---
title: Agentic AI
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_file: app-hf.py
pinned: false
---

# 🤖 Agentic AI - Full-Stack AI Agent System

A full-stack AI agent system with weather, document RAG, web search, and meeting scheduler capabilities, deployed on Hugging Face Spaces.

## 🌟 Features

- **🌤️ Weather Agent**: Real-time weather information using OpenWeatherMap API
- **📄 Document RAG**: Upload and chat with documents (PDF, TXT, DOCX)
- **🔍 Web Search**: DuckDuckGo integration for real-time information
- **📅 Meeting Scheduler**: Create and manage meetings (uses SQLite on HF Spaces)
- **🎨 Modern UI**: Clean, Gemini-like interface with streaming responses

## 🚀 Quick Start - Deploy to HF Spaces

### Prerequisites
- [Hugging Face account](https://huggingface.co/join) (free)
- Git installed locally
- API keys (see below)

### Required API Keys

1. **GROQ_API_KEY** (Required) - Get from [console.groq.com](https://console.groq.com/keys)
   - Free tier: 6,000 requests/minute
   - Powers the AI agent system

2. **OPENWEATHER_API_KEY** (Optional) - Get from [openweathermap.org](https://openweathermap.org/api)
   - Free tier: 1,000 calls/day
   - Enables weather functionality

### Deployment Steps

#### 1. Create a New Space

```bash
# Go to https://huggingface.co/spaces
# Click "Create new Space"
# - Name: agentic-ai (or your choice)
# - Space SDK: Docker
# - Hardware: CPU basic (free)
# - Visibility: Public or Private
# Click "Create Space"
```

#### 2. Clone Your Space

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME
```

#### 3. Copy Files from This Repo

```bash
# From your local agentic-backend directory
cp app-hf.py .
cp requirements-hf.txt .
cp Dockerfile.hf-combined Dockerfile
cp -r backend/ .
cp -r frontend/ .
cp .gitignore .
```

Your space directory should look like:
```
├── Dockerfile
├── requirements-hf.txt
├── app-hf.py
├── backend/
│   ├── __init__.py
│   ├── agents.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── tools.py
├── frontend/
│   ├── __init__.py
│   ├── server.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
└── .git/
```

#### 4. Set Environment Variables (Secrets)

On your HF Space page:
1. Go to **Settings** → **Repository secrets**
2. Add these secrets:

```env
GROQ_API_KEY=your_groq_api_key_here
OPENWEATHER_API_KEY=your_openweather_key_here
```

**Note**: Never commit API keys to your repository!

#### 5. Commit and Push

```bash
git add .
git commit -m "Initial deployment: Agentic AI combined app"
git push
```

#### 6. Wait for Build

- HF Spaces will automatically detect the Dockerfile
- Build typically takes 3-5 minutes
- Watch the **Logs** tab for progress
- Once complete, you'll see "Running" status

#### 7. Test Your App

Your app will be available at:
```
https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space
```

Test these features:
- ✅ Backend status indicator (green = connected)
- ✅ Send a chat message
- ✅ Ask about weather: "What's the weather in London?"
- ✅ Upload a document and ask questions
- ✅ Create a meeting

## 🔄 Force Rebuild / Update

### Method 1: Push Changes (Recommended)
```bash
# Make your changes locally
git add .
git commit -m "Update: describe your changes"
git push
```
HF Spaces will auto-rebuild.

### Method 2: Factory Reboot
1. Go to your Space settings
2. Click **Factory reboot**
3. Confirm - this forces a complete rebuild

### Method 3: Delete & Recreate Build
1. Settings → **Sleep time settings**
2. Enable automatic sleep
3. Wait for space to sleep
4. Click to wake it up - forces rebuild

## 📝 Configuration

### Database
- Uses **SQLite** on HF Spaces (no PostgreSQL needed)
- Database file stored in `/app/agentic.db`
- Persistent across rebuilds (stored in Space storage)

### Ports
- Backend: `8000` (internal)
- Frontend: `7860` (HF Spaces standard port)

### Environment Variables
Can be set in HF Space secrets:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | Yes | - | Groq API key for LLM |
| `OPENWEATHER_API_KEY` | No | - | Weather API key |
| `DEBUG` | No | `False` | Enable debug mode |
| `LOG_LEVEL` | No | `INFO` | Logging level |

## 🐛 Troubleshooting

### Build Fails
- Check the **Logs** tab for specific errors
- Verify all files are present in the repo
- Ensure `Dockerfile` references correct files

### Backend Offline
- Check logs for backend startup errors
- Verify `GROQ_API_KEY` is set correctly
- Try factory reboot to force rebuild

### File Upload Fails
- HF Spaces has file size limits (usually 50MB)
- Check `/app/uploads` directory exists
- Verify proper permissions in Dockerfile

### Missing Dependencies
- Check `requirements-hf.txt` includes all needed packages
- Try adding specific version constraints
- Force rebuild after updating requirements

## 📊 Resource Usage

| Component | CPU | Memory | Disk |
|-----------|-----|--------|------|
| Backend | ~0.2 cores | ~500MB | ~2GB |
| Frontend | ~0.1 cores | ~200MB | ~100MB |
| **Total** | ~0.3 cores | ~700MB | ~2.1GB |

✅ Fits comfortably in HF Spaces **free tier**!

## 🔒 Security Notes

1. **Never commit API keys** - always use HF Secrets
2. **Use private spaces** for sensitive data
3. **Validate file uploads** - the app does basic validation
4. **Rate limiting** - consider adding for production use

## 📚 Additional Resources

- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Docker on HF Spaces](https://huggingface.co/docs/hub/spaces-sdks-docker)
- [Gradio SDK Alternative](https://huggingface.co/docs/hub/spaces-sdks-gradio)

## 🆘 Support

Having issues? Check:
1. HF Space **Logs** tab for errors
2. Verify all secrets are set correctly
3. Try factory reboot
4. Check this README for troubleshooting tips

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built with ❤️ using FastAPI, Flask, LangChain, and Groq**
