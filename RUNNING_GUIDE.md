# Running the Agentic AI Application

## Quick Reference

### 🖥️ Development Mode (Local Testing)

#### Prerequisites
- Python 3.11+ installed
- PostgreSQL running on port 5433
- API keys configured in `.env`

#### Terminal 1: Backend Service
```bash
cd d:\agentic-backend
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Terminal 2: Frontend Service  
```bash
cd d:\agentic-backend
python frontend/server.py
```

#### Access Application
```
Frontend: http://localhost:5000
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs
```

---

### 🐳 Docker Mode (Recommended for Production)

#### Prerequisites
- Docker installed
- Docker Compose installed
- `.env` file with API keys

#### Start All Services
```bash
cd d:\agentic-backend
docker-compose -f docker-compose-full.yml up -d
```

#### Check Services
```bash
docker-compose -f docker-compose-full.yml ps
```

#### View Logs
```bash
# All services
docker-compose -f docker-compose-full.yml logs -f

# Specific service
docker-compose -f docker-compose-full.yml logs -f backend
docker-compose -f docker-compose-full.yml logs -f frontend
docker-compose -f docker-compose-full.yml logs -f postgres
```

#### Stop Services
```bash
docker-compose -f docker-compose-full.yml down
```

---

### 🏃 Production Mode (Using Scripts)

#### Windows
```bash
cd d:\agentic-backend
.\run_production.bat
```

#### Linux/Mac
```bash
cd d:\agentic-backend
bash run_production.sh
```

---

## Detailed Configuration

### Environment Variables (.env)

Create a `.env` file in the root directory:

```env
# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5433
POSTGRES_DB=agentic_db
DATABASE_URL=postgresql+asyncpg://postgres:postgres@127.0.0.1:5433/agentic_db
SYNC_DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5433/agentic_db

# API Keys (Get from respective services)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  # https://console.groq.com
OPENWEATHER_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  # https://openweathermap.org/api

# Optional
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  # For fallback

# Application Settings
ENVIRONMENT=development  # or production
BACKEND_URL=http://localhost:8000  # For production, set to actual domain
DEBUG=True  # False in production
LOG_LEVEL=INFO
```

---

## Accessing the Application

### Development Mode
- **Frontend UI:** http://localhost:5000
- **Backend API:** http://localhost:8000
- **FastAPI Docs:** http://localhost:8000/docs
- **Database:** localhost:5433 (postgres)

### Docker Mode
- **Frontend UI:** http://localhost:5000
- **Backend API:** http://localhost:8000
- **FastAPI Docs:** http://localhost:8000/docs
- **Database:** localhost:5433 (postgres)

---

## Troubleshooting

### Backend Fails to Start
```bash
# Check if port 8000 is in use
netstat -an | grep 8000  # Linux/Mac
netstat -an | findstr 8000  # Windows

# Kill process on port 8000 (if needed)
lsof -ti:8000 | xargs kill -9  # Linux/Mac
netstat -ano | findstr :8000  # Windows (find PID and kill)
```

### Frontend Fails to Connect to Backend
- Check if backend is running: http://localhost:8000/api/health
- Verify BACKEND_URL in .env
- Check firewall settings
- Look at browser console (F12) for errors

### Database Connection Issues
```bash
# Check if PostgreSQL is running
psql -h 127.0.0.1 -p 5433 -U postgres -c "SELECT 1"

# Check database exists
psql -h 127.0.0.1 -p 5433 -U postgres -l
```

### Docker Issues
```bash
# Remove all containers and volumes (careful!)
docker-compose -f docker-compose-full.yml down -v

# Rebuild images
docker-compose -f docker-compose-full.yml build --no-cache

# Start fresh
docker-compose -f docker-compose-full.yml up -d
```

---

## Checking Service Health

### Backend Health Check
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-01-02T10:30:00"
}
```

### Frontend Health Check
```bash
curl http://localhost:5000
```

Expected: Returns HTML page (200 OK)

---

## Testing the API

### Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the weather today?"}'
```

### Meetings Endpoint
```bash
curl http://localhost:8000/api/meetings?date=today
```

### Through Frontend
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the weather today?"}'
```

---

## Performance Tips

### Development
- Use `--reload` flag for auto-restart on code changes
- Keep browser DevTools open for debugging
- Use curl/Postman for API testing

### Production (Docker)
- Set `DEBUG=False` in .env
- Use multiple workers: `gunicorn -w 4` (default)
- Enable caching for static assets
- Monitor logs regularly

### Database
- Run backups regularly
- Monitor connection pool usage
- Check slow query logs
- Vacuum and analyze tables periodically

---

## Deployment Checklist

- [ ] .env file configured with all API keys
- [ ] PostgreSQL database running and accessible
- [ ] Backend starts without errors
- [ ] Frontend starts and connects to backend
- [ ] Health check endpoints respond
- [ ] Chat endpoint works
- [ ] File upload works
- [ ] Meetings create successfully
- [ ] All quick action buttons work
- [ ] Responsive design works on mobile

---

## Support & Debugging

### Enable Debug Logging
In `.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### View All Logs
```bash
# Backend
docker logs -f agentic_backend

# Frontend
docker logs -f agentic_frontend

# Database
docker logs -f agentic_postgres
```

### Test Individual Components

**Database:**
```python
from backend.database import test_connection
import asyncio
result = asyncio.run(test_connection())
print(f"DB Connected: {result}")
```

**Backend API:**
```bash
python -m pytest backend/tests/  # If tests exist
```

**Frontend:**
```bash
# Open browser console (F12) and check for errors
```

---

## Next Steps

1. **Configure API Keys:** Add GROQ_API_KEY and OPENWEATHER_API_KEY to .env
2. **Start Services:** Run backend and frontend (development) or Docker (production)
3. **Test Application:** Visit http://localhost:5000 and try asking questions
4. **Upload Document:** Test RAG feature by uploading a PDF
5. **Create Meetings:** Test meeting scheduling functionality
6. **Deploy to Cloud:** Follow DEPLOYMENT_GUIDE.md for Render, Railway, or Heroku

Good luck! 🚀
