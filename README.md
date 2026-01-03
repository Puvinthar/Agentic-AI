# 🤖 Agentic AI - Full Stack

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2.28-orange.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-yellow.svg)

An **intelligent, production-ready Agentic AI system** that autonomously reasons, decides which tools to use, fetches data, and responds naturally. Built with **FastAPI**, **LangGraph**, and **PostgreSQL**, featuring 4 specialized AI agents with a modern ChatGPT-inspired interface.

## 🚀 Live Demo

**Try it now:** [https://huggingface.co/spaces/lossleo/Agentic-AI-fullstack](https://huggingface.co/spaces/lossleo/Agentic-AI-fullstack)

**Note:** API documentation is available when running locally at `http://localhost:8000/docs`

---

## 🌟 Features

### 🎨 **Modern ChatGPT-Inspired UI**
- Professional purple/indigo gradient design
- Light/Dark theme toggle
- Responsive card-based capability showcase
- Real-time backend status indicator
- Markdown rendering for rich responses

### 🧠 **4 Intelligent Agents**

#### 1️⃣ **Weather Intelligence Agent** 🌤️
- Natural language weather queries
- Supports past, current, and future weather
- OpenWeatherMap API integration

**Examples:**
```
"What is the weather in Chennai today?"
"What was the weather in Bengaluru yesterday?"
"What will the weather be like in London tomorrow?"
```

#### 2️⃣ **Document Understanding + Web Intelligence Agent** 📄
- Upload and analyze PDF/TXT documents
- RAG (Retrieval Augmented Generation) for Q&A
- Automatic fallback to web search if answer not in document
- FAISS vector store for semantic search

**Examples:**
```
Upload: company_policy.pdf
Query: "What is the leave policy?" → Answers from document
Query: "Who is the CEO of Google?" → Searches web
```

#### 3️⃣ **Meeting Scheduling + Weather Reasoning Agent** 📅
- Intelligent meeting scheduling based on weather conditions
- Checks existing meetings in database
- Creates meetings only if weather is suitable
- Beautiful tabular response format
- Duplicate detection and smart recommendations

**Examples:**
```
"Schedule a meeting in Chennai at 5pm if weather is good"
"Create a review meeting tomorrow in Bangalore"
```

**Response Format:**
- Weather forecast with emoji indicators
- Analysis table (Status & Condition)
- Meeting details table (Title, Date, Time, Location)
- Smart recommendations for bad weather

#### 4️⃣ **Natural Language → Database Query Agent** 🗄️
- Converts natural language to SQL queries
- Understands temporal queries (today, tomorrow, next week)
- Pattern learning for complex queries

**Examples:**
```
"Show all meetings scheduled tomorrow"
"Do we have any meetings today?"
"List meetings next week"
"Is there any review meeting?"
```

---

## 🏗️ Architecture

```
User Question
     ↓
🤖 AI Reasoning Agent (LangGraph)
     ↓
  Intent Classification
     ↓
┌────────────────────────────────┐
│  Weather  │  Document  │  DB   │
│   Tool    │    RAG     │ Tool  │
│           │  + Search  │       │
└────────────────────────────────┘
     ↓
Execute Action
     ↓
Generate Natural Response (LLM)
     ↓
Return to User
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Flask + Vanilla JavaScript |
| **UI Framework** | Inter Font, CSS Variables |
| **Backend Framework** | FastAPI |
| **Agentic Orchestration** | LangGraph |
| **LLM** | Groq (llama-3.1-70b-versatile) |
| **Database** | Neon PostgreSQL (Cloud) |
| **ORM** | SQLAlchemy (Async) + asyncpg |
| **Vector Store** | FAISS |
| **Embeddings** | HuggingFace sentence-transformers |
| **Document Processing** | PyPDF, LangChain |
| **Web Search** | DuckDuckGo |
| **Weather API** | OpenWeatherMap |
| **Deployment** | Hugging Face Spaces (Docker) |

---

## 📁 Project Structure

```
agentic-backend/
│
├── backend/
│   ├── main.py              # FastAPI entry point & API endpoints
│   ├── agents.py            # LangGraph agentic logic (4 agents)
│   ├── tools.py             # Tool definitions (Weather, RAG, Search, DB)
│   ├── models.py            # SQLAlchemy database models
│   └── database.py          # PostgreSQL connection & async sessions
│
├── frontend/
│   ├── server.py            # Flask frontend server
│   ├── templates/
│   │   └── index.html       # Main UI (ChatGPT-inspired)
│   └── static/
│       ├── css/
│       │   └── style.css    # Professional purple/indigo theme
│       └── js/
│           └── app.js       # Frontend logic & API calls
│
├── uploads/                 # Document upload directory
├── requirements.txt         # Python dependencies
├── Dockerfile.hf            # Hugging Face Space Docker config
├── app-hf.py               # Combined app for HF deployment
├── .env.example            # Environment variables template
│
└── docs/                   # Documentation
    ├── START_HERE.md
    ├── QUICK_START_DEPLOYMENT.md
    └── PROJECT_STRUCTURE.md
```

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.11+
- Neon PostgreSQL account (free tier)
- API Keys:
  - [Groq API](https://console.groq.com/) (Free & Fast)
  - [OpenWeatherMap API](https://openweathermap.org/api) (Free tier)

### **Method 1: Try Live Demo** 🌐

Visit: [https://huggingface.co/spaces/lossleo/Agentic-AI-fullstack](https://huggingface.co/spaces/lossleo/Agentic-AI-fullstack)

**Features:**
- ✅ No setup required
- ✅ ChatGPT-inspired interface
- ✅ Light/Dark theme toggle
- ✅ All 4 agents ready to use
- ✅ Document upload & RAG
- ✅ Weather-based meeting scheduling

### **Method 2: Local Setup**

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Puvinthar/Agentic-AI.git
cd Agentic-AI
```

#### 2️⃣ Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4️⃣ Set Up Environment Variables
```bash
# Copy template
cp .env.example .env

# Edit .env with your credentials:
# DATABASE_URL=postgresql+asyncpg://user:pass@host/dbname
# GROQ_API_KEY=gsk_your_groq_api_key
# OPENWEATHER_API_KEY=your_openweather_api_key
```

**Get Neon PostgreSQL URL:**
1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy connection string (use pooled connection)
4. Replace `postgresql://` with `postgresql+asyncpg://`

#### 5️⃣ Run the Application
```bash
# Start backend
cd backend
python main.py

# In another terminal, start frontend
cd frontend
python server.py
```

#### 6️⃣ Access the Application
- **Frontend UI:** http://localhost:7860
- **Backend API:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/health

---

### **Method 3: Deploy to Hugging Face Spaces** 🤗

#### 1️⃣ Create New Space
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose **Docker** as SDK
4. Clone the space repository

#### 2️⃣ Push Code
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME
cp -r path/to/Agentic-AI/* .
git add .
git commit -m "Initial deployment"
git push
```

#### 3️⃣ Add Secrets
In Space Settings → Repository Secrets, add:
- `DATABASE_URL` - Your Neon PostgreSQL connection string
- `GROQ_API_KEY` - Your Groq API key
- `OPENWEATHER_API_KEY` - Your OpenWeather API key

#### 4️⃣ Wait for Build
Space will automatically build and deploy (2-3 minutes)

**Your app will be live at:** `https://huggingface.co/spaces/USERNAME/SPACE_NAME`

---

## 🔗 API Documentation

### **Swagger UI (Interactive)**
- **Local:** http://localhost:8000/docs
- **Note:** Backend API runs internally on HF Spaces and is accessed through the frontend

### **ReDoc (Documentation)**
- **Local:** http://localhost:8000/redoc

---

## 📡 API Endpoints

### **Base URLs**
- **Live:** `https://lossleo-agentic-ai-fullstack.hf.space/api`
- **Local:** `http://localhost:8000/api`

### **1. Chat Endpoint** 💬
```bash
POST /api/chat
Content-Type: application/json

{
  "query": "Schedule a meeting in Chennai at 5pm if weather is good"
}
```

**Response:**
```json
{
  "response": "🌤️ Weather Forecast for Chennai...\n\n### ☁️ Weather Analysis\n| Status | Condition |\n|--------|-----------|...",
  "timestamp": "2026-01-03T10:30:00"
}
```

### **2. Upload Document** 📄
```bash
POST /api/upload
Content-Type: multipart/form-data

file: your_document.pdf
```

### **3. Get Meetings** 📅
```bash
GET /api/meetings?date=tomorrow
```

### **4. Create Meeting** ➕
```bash
POST /api/meetings
Content-Type: application/json

{
  "title": "Team Standup",
  "scheduled_date": "2026-01-02T10:00:00",
  "location": "Conference Room A",
  "description": "Daily sync"
}
```

### **5. Health Check** ✅
```bash
GET /api/health
```

---

## 🎯 Usage Examples

### **Example 1: Weather Query**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the weather in Chennai today?"}'
```

### **Example 2: Document Q&A**
```bash
# Upload document
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@resume.pdf"

# Ask question
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are my technical skills?"}'
```

### **Example 3: Meeting Scheduling with Weather**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "Schedule a team meeting if tomorrow\'s weather is good in Bangalore"}'
```

### **Example 4: Database Query**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "Show all meetings scheduled tomorrow"}'
```

---

## 🧪 Testing

### **Test with cURL**
```bash
# Health check
curl http://localhost:8000/api/health

# Chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "test query"}'
```

### **Test with Python**
```python
import requests

# Chat endpoint
response = requests.post(
    "http://localhost:8000/api/chat",
    json={"query": "What is the weather in Chennai?"}
)
print(response.json())
```

---

## 🔧 Configuration

### **Environment Variables**

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection (async) | Yes |
| `SYNC_DATABASE_URL` | PostgreSQL connection (sync) | Yes |
| `GROQ_API_KEY` | Groq API key for LLM | Recommended |
| `OPENAI_API_KEY` | OpenAI API key (alternative) | Optional |
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | Yes |
| `DEBUG` | Enable debug mode | No |
| `LOG_LEVEL` | Logging level | No |

---

## 🎨 Innovative Features

### **What Makes This Project Stand Out:**

1. **🧠 True Agentic Behavior**
   - Intelligent intent classification
   - Dynamic tool selection
   - Multi-step reasoning (Agent 3)

2. **🔄 Hybrid RAG + Web Search**
   - Document Q&A with automatic web fallback
   - Semantic search using FAISS embeddings

3. **🌤️ Weather-Based Decision Making**
   - Agent analyzes weather conditions
   - Makes logical decisions (good/bad weather)
   - Schedules meetings intelligently

4. **🗣️ Natural Language to SQL**
   - Understands temporal queries
   - Pattern learning for complex queries
   - No manual SQL writing needed

5. **📦 Production-Ready**
   - Docker support
   - Async database operations
   - Comprehensive error handling
   - Structured logging
   - API documentation

6. **🎯 Modular Architecture**
   - Easy to extend with new agents
   - Clean separation of concerns
   - Type hints throughout

---

## 📊 Database Schema

### **Meetings Table**
```sql
CREATE TABLE meetings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    scheduled_date TIMESTAMP NOT NULL,
    location VARCHAR(255),
    weather_condition VARCHAR(100),
    is_weather_dependent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### **Documents Table**
```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(500) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    upload_date TIMESTAMP DEFAULT NOW(),
    processed BOOLEAN DEFAULT FALSE
);
```

---

## 🐛 Troubleshooting

### **Issue: Database Connection Failed**
```bash
# Check if PostgreSQL is running
docker ps

# Check connection string in .env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/agentic_db
```

### **Issue: LLM Not Responding**
```bash
# Verify API key in .env
GROQ_API_KEY=your_actual_api_key

# Check logs
docker-compose logs backend
```

### **Issue: Document Upload Fails**
```bash
# Ensure uploads directory exists
mkdir uploads

# Check file permissions
chmod 755 uploads
```

---

## 🚀 Deployment

### **Deploy to Cloud**

#### **Heroku**
```bash
heroku create agentic-backend
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

#### **Railway**
1. Connect GitHub repository
2. Add PostgreSQL service
3. Set environment variables
4. Deploy

#### **AWS ECS**
1. Build Docker image
2. Push to ECR
3. Create ECS task definition
4. Deploy to Fargate

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 👤 Author

**Puvinthar Stephen**
- **GitHub:** [@Puvinthar](https://github.com/Puvinthar)
- **Hugging Face:** [@lossleo](https://huggingface.co/lossleo)
- **Live Demo:** [Agentic AI Fullstack](https://huggingface.co/spaces/lossleo/Agentic-AI-fullstack)

---

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) - LLM framework
- [LangGraph](https://github.com/langchain-ai/langgraph) - Agentic orchestration
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Groq](https://groq.com/) - Ultra-fast LLM inference
- [OpenWeatherMap](https://openweathermap.org/) - Weather data
- [Neon](https://neon.tech/) - Serverless PostgreSQL
- [Hugging Face](https://huggingface.co/) - Hosting platform

---

## 📞 Support

If you have any questions or issues:
- Open an issue on [GitHub](https://github.com/Puvinthar/Agentic-AI/issues)
- Try the [Live Demo](https://huggingface.co/spaces/lossleo/Agentic-AI-fullstack)

---

## ⭐ Show Your Support

If this project helped you, please give it a ⭐️!

---

<div align="center">
  
### 🌟 **Live Demo**
**[Try Agentic AI Now →](https://huggingface.co/spaces/lossleo/Agentic-AI-fullstack)**

*(API documentation available when running locally)*

---

**Built with ❤️ by Puvinthar Stephen**

*Powered by FastAPI, LangGraph, Groq LLM, and Neon PostgreSQL*

**⭐ Star this repo if it helped you!**

</div>
