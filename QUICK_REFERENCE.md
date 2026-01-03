# 🚀 Quick Reference Card

## Project Structure at a Glance

```
FRONTEND (Port 5000)              BACKEND (Port 8000)
    ↓                                   ↓
[Flask Web Server]          [FastAPI REST API]
    ↓                                   ↓
[HTML/CSS/JS UI]            [4 AI Agents]
    ↓                                   ↓
[Gemini-like Interface] ←API→ [PostgreSQL Database]
```

---

## 📂 Where Everything Is

### Backend Logic
| What | Where | Type |
|------|-------|------|
| REST API endpoints | `backend/main.py` | Python (FastAPI) |
| Database setup | `backend/database.py` | Python |
| AI agents | `backend/agents.py` | Python (LangGraph) |
| Tools & integrations | `backend/tools.py` | Python |
| Data models | `backend/models.py` | Python (SQLAlchemy) |

### Frontend UI
| What | Where | Type |
|------|-------|------|
| Web server | `frontend/server.py` | Python (Flask) |
| HTML page | `frontend/templates/index.html` | HTML |
| Styling | `frontend/static/css/style.css` | CSS |
| Interactions | `frontend/static/js/app.js` | JavaScript |

---

## ⚡ Commands You'll Use

### Start for Development
```bash
# Terminal 1 - Backend
cd d:\agentic-backend
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend
cd d:\agentic-backend
python frontend/server.py

# Visit: http://localhost:5000
```

### Start for Production
```bash
cd d:\agentic-backend
docker-compose -f docker-compose-full.yml up -d

# Visit: http://localhost:5000
```

### Stop Everything
```bash
docker-compose -f docker-compose-full.yml down
```

### Check Logs
```bash
docker-compose -f docker-compose-full.yml logs -f
```

---

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Health check |
| `/api/chat` | POST | Ask the AI |
| `/api/upload` | POST | Upload document |
| `/api/meetings` | GET | List meetings |
| `/api/meetings` | POST | Create meeting |

### Example Requests
```bash
# Chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the weather?"}'

# Health
curl http://localhost:8000/api/health

# Meetings
curl http://localhost:8000/api/meetings?date=today
```

---

## 📝 Configuration

### File: `.env`
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5433
GROQ_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_key_here
ENVIRONMENT=development  # or production
```

---

## 📊 Service Ports

| Service | Port | Purpose |
|---------|------|---------|
| Frontend | 5000 | Web UI |
| Backend | 8000 | REST API |
| Database | 5433 | PostgreSQL |

---

## 🎯 Quick Navigation

### Need to change AI behavior?
→ Edit `backend/agents.py`

### Need to change UI?
→ Edit `frontend/templates/index.html`

### Need to change styling?
→ Edit `frontend/static/css/style.css`

### Need to add new API endpoint?
→ Add to `backend/main.py`

### Need to change database?
→ Edit `backend/models.py`

### Need to add new tool?
→ Add to `backend/tools.py`

---

## 🔍 Troubleshooting Fast

| Problem | Solution |
|---------|----------|
| Backend won't start | Check port 8000 is free, check .env file |
| Frontend won't connect | Make sure backend is running, check BACKEND_URL |
| Database error | Check PostgreSQL is running on port 5433 |
| Import errors | Check `backend/` prefix in imports |
| Docker issues | Run `docker-compose ... build --no-cache` |

---

## 📦 Key Technologies

| Component | Tech | Version |
|-----------|------|---------|
| Backend Web | FastAPI | Latest |
| Frontend Web | Flask | Latest |
| Database | PostgreSQL | 15 |
| AI/LLM | Groq API | Latest |
| Agent Framework | LangGraph | Latest |
| Container | Docker | Latest |
| Vector DB | FAISS | Latest |

---

## 🔐 Security Checklist

- ✅ API keys in .env (not in code)
- ✅ CORS configured
- ✅ Input validation on all endpoints
- ✅ Error messages don't leak info
- ✅ Database in private container network
- ✅ HTTPS ready (configure in production)

---

## 📈 Performance Tips

**Development:**
- Use `--reload` for auto-restart
- Keep DevTools open (F12)

**Production:**
- Set `DEBUG=False`
- Use multiple workers (4+)
- Enable caching
- Monitor logs

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Main overview |
| `RUNNING_GUIDE.md` | How to run |
| `STRUCTURE_REORGANIZATION.md` | What changed |
| `PROJECT_STRUCTURE_OVERVIEW.md` | Visual guide |
| `docs/PROJECT_STRUCTURE.md` | Deep dive |
| `DEPLOYMENT_GUIDE.md` | Cloud deployment |

---

## ✨ Features at a Glance

- 🤖 4 intelligent AI agents
- 🌤️ Weather intelligence
- 📄 Document RAG with web search
- 📅 Smart meeting scheduling
- 🗄️ Natural language database queries
- 🎨 Modern Gemini-like UI
- 📱 Fully responsive design
- 🐳 Docker containerized
- 📊 Production ready
- ⚡ Fast & scalable

---

## 🎓 Learning Path

1. Start with `RUNNING_GUIDE.md`
2. Read `PROJECT_STRUCTURE_OVERVIEW.md`
3. Look at `docs/PROJECT_STRUCTURE.md`
4. Explore code in `backend/` and `frontend/`
5. Read `DEPLOYMENT_GUIDE.md` when ready to deploy

---

## 🚀 Get Started Now

```bash
# 1. Configure .env with your API keys
# 2. Start services
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
python frontend/server.py
# 3. Visit http://localhost:5000
# 4. Start chatting!
```

---

**Questions?** Check the documentation files listed above.  
**Issues?** See Troubleshooting section.  
**Ready to deploy?** See DEPLOYMENT_GUIDE.md.

Happy coding! 🎉
