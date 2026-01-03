# Project Structure Guide

## 📁 Directory Organization

```
agentic-backend/
│
├── 📂 backend/                    # FastAPI Backend Microservice
│   ├── __init__.py               # Package initialization
│   ├── main.py                   # FastAPI app & all endpoints
│   ├── database.py               # PostgreSQL connection & session management
│   ├── models.py                 # SQLAlchemy ORM models (Meeting, DocumentMetadata)
│   ├── agents.py                 # LangGraph agentic workflow
│   └── tools.py                  # Tool definitions (Weather, RAG, Search, Meetings)
│
├── 📂 frontend/                   # Flask Frontend Web Server
│   ├── __init__.py               # Package initialization
│   ├── server.py                 # Flask app with API proxy endpoints
│   ├── 📂 templates/
│   │   └── index.html            # Main HTML interface (Gemini-like design)
│   └── 📂 static/
│       ├── 📂 css/
│       │   └── style.css         # Modern dark theme styling
│       └── 📂 js/
│           └── app.js            # Frontend logic & API communication
│
├── 📂 shared/                     # Shared utilities (for future use)
│   └── (config, utilities, etc.)
│
├── 📂 uploads/                    # Document storage for RAG
│   └── (user uploaded files)
│
├── 📂 docs/                       # Documentation
│   └── PROJECT_STRUCTURE.md       # This file
│
├── .env                           # Environment variables (Database, API keys)
├── .env.example                   # Example environment file
├── requirements.txt               # Root dependencies
├── docker-compose.yml             # Docker orchestration
├── docker-compose-full.yml        # Production Docker setup
├── Dockerfile                     # Backend Docker image
├── Dockerfile.frontend            # Frontend Docker image
├── run_production.sh              # Production startup script (Linux/Mac)
├── run_production.bat             # Production startup script (Windows)
│
└── README.md                      # Main project documentation
```

## 🏗️ Architecture Overview

### Backend (port 8000)
- **FastAPI** async web framework
- **PostgreSQL** database with asyncpg driver
- **LangGraph** agentic workflow engine
- **4 Intelligent Agents:**
  1. Weather Intelligence (OpenWeatherMap API)
  2. Document RAG + Web Search (FAISS + DuckDuckGo)
  3. Meeting Scheduler (Weather-aware)
  4. Database Query (Natural language)

### Frontend (port 5000)
- **Flask** lightweight web server
- **Vanilla JavaScript** (no framework dependencies)
- **Modern CSS** with dark gradient theme
- **Responsive Design** (works on desktop and mobile)
- **Dynamic Backend URL** (works locally and in production)

## 📦 Key Files Explanation

### Backend

#### `main.py`
- FastAPI application entry point
- RESTful API endpoints:
  - `POST /api/chat` - Process queries through agents
  - `POST /api/upload` - Upload documents for RAG
  - `GET /api/meetings` - Retrieve meetings
  - `POST /api/meetings` - Create meetings
  - `GET /api/health` - Health check
- Database lifespan management
- Error handling and logging

#### `database.py`
- PostgreSQL connection pooling
- Async session factory for FastAPI
- Sync session factory for tools
- Database initialization
- Connection testing

#### `models.py`
- SQLAlchemy ORM models:
  - `Meeting` - Scheduled meetings with weather conditions
  - `DocumentMetadata` - Uploaded document tracking

#### `agents.py`
- **Intent Classifier** - Routes queries to appropriate agent
- **Weather Agent** - Fetches weather data
- **Document Agent** - RAG queries with web fallback
- **Meeting Scheduler** - Creates weather-aware meetings
- **Database Agent** - Natural language database queries
- **Response Generator** - Formats responses with LLM (Groq/OpenAI)
- **LangGraph Workflow** - Orchestrates agent execution

#### `tools.py`
- **Weather Tool** - OpenWeatherMap API integration
- **Document Tool** - FAISS vector store for RAG
- **Web Search Tool** - DuckDuckGo search
- **Meetings Tool** - Database queries

### Frontend

#### `server.py`
- Flask web server
- API proxy endpoints that forward to backend:
  - `/api/chat` → `BACKEND_URL/api/chat`
  - `/api/upload` → `BACKEND_URL/api/documents/upload`
  - `/api/meetings` → `BACKEND_URL/api/meetings`
  - `/api/health` → `BACKEND_URL/api/health`
- Dynamic backend URL configuration
- Development and production modes

#### `templates/index.html`
- Single-page HTML interface
- Sidebar with chat history
- Main chat display area
- Input field with file attachment
- Quick action buttons
- Meeting scheduling modal
- Backend URL passed from Flask context

#### `static/css/style.css`
- 700+ lines of modern CSS
- Dark theme (#1a1a1a background)
- Gradient purple buttons (#667eea → #764ba2)
- Responsive layout
- Mobile-friendly (768px breakpoint)
- Smooth animations
- Custom scrollbars

#### `static/js/app.js`
- Frontend application logic
- Message handling and display
- File upload management
- Meeting creation
- Backend health checking
- Dynamic backend URL detection
- Chat history management

## 🔄 Data Flow

```
User Input (Frontend)
        ↓
   [app.js]
        ↓
  /api/chat (Frontend)
        ↓
  server.py (Flask)
        ↓
  Backend URL Proxy
        ↓
  main.py (FastAPI)
        ↓
  [agents.py] ← routes based on intent
        ↓
[tools.py] ← executes appropriate tool
        ↓
 Response Generation
        ↓
 User Interface (Display)
```

## 🚀 Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
cd d:\agentic-backend
C:\Python313\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd d:\agentic-backend
C:\Python313\python.exe frontend/server.py
```

### Production Mode

**Using run_production.bat (Windows):**
```bash
cd d:\agentic-backend
.\run_production.bat
```

**Using Docker:**
```bash
cd d:\agentic-backend
docker-compose -f docker-compose-full.yml up -d
```

## 🔧 Configuration

### Environment Variables (.env)
```
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5433
POSTGRES_DB=agentic_db
DATABASE_URL=postgresql+asyncpg://...
SYNC_DATABASE_URL=postgresql://...

# APIs
GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=optional
OPENWEATHER_API_KEY=your_weather_key

# Frontend
ENVIRONMENT=development  # or production
BACKEND_URL=http://localhost:8000

# Other
DEBUG=False
LOG_LEVEL=INFO
```

## 📊 Dependencies

### Backend
- fastapi, uvicorn (async web)
- sqlalchemy, asyncpg, psycopg2 (database)
- langchain, langgraph (AI agents)
- langchain-groq, langchain-openai (LLMs)
- faiss-cpu (embeddings)
- requests (HTTP)
- python-dotenv

### Frontend
- flask, flask-cors (web server)
- requests (API calls)
- python-dotenv (config)
- (Frontend JS: vanilla, no dependencies)

## ✨ Key Features

✅ **Separation of Concerns** - Backend and frontend are independent  
✅ **Microservices Ready** - Can be deployed separately  
✅ **Production Ready** - Uses Gunicorn, proper error handling  
✅ **Easy to Scale** - Clear module organization  
✅ **Well Documented** - Code comments throughout  
✅ **Responsive Design** - Works on all screen sizes  
✅ **Dynamic Configuration** - Works in dev and production  
✅ **Docker Support** - Full containerization  

## 🔐 Security Notes

- CORS is enabled (configure origins in production)
- Database credentials from environment variables
- API keys from environment variables
- Input validation on all endpoints
- Error handling doesn't expose sensitive data

## 📈 Future Improvements

- Add authentication/authorization
- Implement request logging middleware
- Add database migrations system
- Create API documentation (Swagger)
- Add comprehensive test suite
- Implement caching layer
- Add WebSocket support for real-time updates
