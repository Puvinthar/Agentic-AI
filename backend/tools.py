"""
Tool Definitions for Agentic AI Backend
Contains all tools: Weather, Document RAG, Google Search, Database Query
"""
import os
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import requests
from langchain_core.tools import Tool
from duckduckgo_search import DDGS
from sqlalchemy import select, and_, or_, func
from backend.database import get_sync_session
from backend.models import Meeting
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Global vector store for document RAG
vector_store = None
document_content = ""

# Lazy imports for heavy ML dependencies to speed up startup
_embeddings = None
_FAISS = None
_text_splitter_class = None
_pdf_loader_class = None
_text_loader_class = None

def _get_embeddings():
    """Lazy load embeddings model"""
    global _embeddings
    if _embeddings is None:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        _embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return _embeddings

def _get_faiss():
    """Lazy load FAISS"""
    global _FAISS
    if _FAISS is None:
        from langchain_community.vectorstores import FAISS
        _FAISS = FAISS
    return _FAISS

def _get_text_splitter():
    """Lazy load text splitter"""
    global _text_splitter_class
    if _text_splitter_class is None:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        _text_splitter_class = RecursiveCharacterTextSplitter
    return _text_splitter_class

def _get_loaders():
    """Lazy load document loaders"""
    global _pdf_loader_class, _text_loader_class
    if _pdf_loader_class is None or _text_loader_class is None:
        from langchain_community.document_loaders import PyPDFLoader, TextLoader
        _pdf_loader_class = PyPDFLoader
        _text_loader_class = TextLoader
    return _pdf_loader_class, _text_loader_class


# ============================================================================
# TOOL 1: WEATHER INTELLIGENCE AGENT
# ============================================================================

def get_weather_tool(location: str, date_query: str = "today") -> str:
    """
    Fetch weather information from OpenWeatherMap API
    
    Args:
        location: City name (e.g., "Chennai", "London")
        date_query: "today", "yesterday", "tomorrow"
    
    Returns:
        Formatted weather information
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key or api_key == "your_openweather_api_key_here":
        return "⚠️ OpenWeatherMap API key not configured. Please set OPENWEATHER_API_KEY in .env file."
    
    try:
        # Determine date offset
        date_offset = 0
        if "yesterday" in date_query.lower():
            date_offset = -1
        elif "tomorrow" in date_query.lower():
            date_offset = 1
        
        target_date = datetime.now() + timedelta(days=date_offset)
        
        # For current/past weather (yesterday, today)
        if date_offset <= 0:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                weather = {
                    "location": data["name"],
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"],
                    "date": target_date.strftime("%Y-%m-%d"),
                }
                
                result = f"""
🌤️ Weather Information for {weather['location']}
📅 Date: {weather['date']}
🌡️ Temperature: {weather['temperature']}°C (Feels like {weather['feels_like']}°C)
☁️ Condition: {weather['description'].title()}
💧 Humidity: {weather['humidity']}%
💨 Wind Speed: {weather['wind_speed']} m/s
                """
                return result.strip()
            else:
                return f"❌ Could not fetch weather for {location}. Error: {response.json().get('message', 'Unknown error')}"
        
        # For future weather (tomorrow and beyond)
        else:
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # Get forecast for tomorrow (closest to noon)
                forecast_list = data["list"]
                target_forecast = forecast_list[8] if len(forecast_list) > 8 else forecast_list[0]
                
                weather = {
                    "location": data["city"]["name"],
                    "temperature": target_forecast["main"]["temp"],
                    "feels_like": target_forecast["main"]["feels_like"],
                    "humidity": target_forecast["main"]["humidity"],
                    "description": target_forecast["weather"][0]["description"],
                    "wind_speed": target_forecast["wind"]["speed"],
                    "date": target_date.strftime("%Y-%m-%d"),
                }
                
                result = f"""
🌤️ Weather Forecast for {weather['location']}
📅 Date: {weather['date']}
🌡️ Temperature: {weather['temperature']}°C (Feels like {weather['feels_like']}°C)
☁️ Condition: {weather['description'].title()}
💧 Humidity: {weather['humidity']}%
💨 Wind Speed: {weather['wind_speed']} m/s
                """
                return result.strip()
            else:
                return f"❌ Could not fetch weather forecast for {location}. Error: {response.json().get('message', 'Unknown error')}"
                
    except Exception as e:
        logger.error(f"Weather API error: {e}")
        return f"❌ Error fetching weather: {str(e)}"


# ============================================================================
# TOOL 2: DOCUMENT UNDERSTANDING (RAG)
# ============================================================================

def load_document_tool(file_path: str) -> str:
    """
    Load and process a document for RAG (Retrieval Augmented Generation)
    
    Args:
        file_path: Path to PDF or text file
    
    Returns:
        Status message
    """
    global vector_store, document_content
    
    try:
        # Lazy load dependencies
        PyPDFLoader, TextLoader = _get_loaders()
        
        # Load document based on file type
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path)
        else:
            return "❌ Unsupported file format. Please upload PDF or TXT files."
        
        documents = loader.load()
        document_content = "\n".join([doc.page_content for doc in documents])
        
        # Split text into chunks
        RecursiveCharacterTextSplitter = _get_text_splitter()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_documents(documents)
        
        # Create embeddings and vector store
        embeddings = _get_embeddings()
        FAISS = _get_faiss()
        vector_store = FAISS.from_documents(chunks, embeddings)
        
        logger.info(f"✅ Document loaded: {len(chunks)} chunks created")
        return f"✅ Document processed successfully! Created {len(chunks)} text chunks for querying."
        
    except Exception as e:
        logger.error(f"Document loading error: {e}", exc_info=True)
        return f"❌ Error loading document: {str(e)}"


def query_document_tool(question: str) -> str:
    """
    Intelligent document query using semantic search + LLM reasoning
    Now handles questions like "Does he know coding?" by understanding context
    
    Args:
        question: User's question about the document
    
    Returns:
        Intelligent answer generated by LLM from relevant document sections
    """
    global vector_store, document_content
    
    if vector_store is None:
        return "❌ No document loaded. Please upload a document first using /api/upload endpoint."
    
    if not document_content:
        return "❌ Document content is empty. Please upload a valid document."
    
    try:
        question = question.strip()
        if not question:
            return "❌ Please provide a valid question."
        
        # Strategy: For small documents (< 5000 chars), use full context
        # For larger docs, use semantic search with LLM reasoning
        
        if len(document_content) < 5000:
            # FULL CONTEXT APPROACH - Best for resumes/short docs
            from langchain_groq import ChatGroq
            import os
            
            groq_api_key = os.getenv("GROQ_API_KEY")
            if groq_api_key and groq_api_key != "your_groq_api_key_here":
                try:
                    llm = ChatGroq(
                        groq_api_key=groq_api_key,
                        model_name="llama-3.1-70b-versatile",
                    temperature=0.2,  # Low for precision, not creativity

<RESUME_CONTEXT>
{document_content}
</RESUME_CONTEXT>

--- CRITICAL INSTRUCTIONS FOR AI ---
⚠️ DO NOT COPY-PASTE FROM THE RESUME
⚠️ DO NOT DUMP ENTIRE SECTIONS
⚠️ THINK BEFORE YOU SPEAK

**STEP 1 - ANALYSIS:** Read the resume and identify ONLY the specific details that answer: "{question}"

**STEP 2 - SYNTHESIS:** Create a meaningful, concise answer by:
• Extracting 2-4 key points (NOT everything)
• Using your OWN professional wording
• Being selective and strategic

**STEP 3 - FORMATTING:**
• Use bullet points ONLY for lists of 3+ items
• Keep each point under 12 words
• Professional, direct tone

**STEP 4 - RESTRICTION:**
• Maximum 100 words total
• If info not in resume → say "This information is not mentioned"
• Focus on what matters MOST for the question

--- USER QUESTION ---
{question}

--- YOUR INTELLIGENT ANSWER (MAX 100 WORDS) ---"""
                    
                    response = llm.invoke(prompt)
                    answer = response.content.strip()
                    
                    return f"""📄 **Answer from Document**

{answer}

---
💡 *Ask specific questions like "What are his skills?" or "Tell me about his experience"*"""
                except Exception as e:
                    logger.warning(f"LLM processing failed: {e}, falling back to semantic search")
        
        # SEMANTIC SEARCH APPROACH - For larger documents or LLM fallback
        relevant_docs_with_scores = vector_store.similarity_search_with_score(question, k=5)
        
        if not relevant_docs_with_scores:
            return "⚠️ No relevant information found in the document. Try rephrasing your question."
        
        # Use top 4 most relevant chunks (increased from 3)
        RELEVANCE_THRESHOLD = 2.0
        filtered_docs = [(doc, score) for doc, score in relevant_docs_with_scores if score < RELEVANCE_THRESHOLD]
        
        if not filtered_docs:
            filtered_docs = relevant_docs_with_scores[:3]
        
        top_docs = [doc for doc, score in sorted(filtered_docs, key=lambda x: x[1])[:4]]
        
        # Extract and combine context
        context_parts = []
        for doc in top_docs:
            content = doc.page_content.strip()
            if content:
                lines = content.split('\n')
                cleaned_lines = [line.strip() for line in lines if line.strip()]
                clean_content = '\n'.join(cleaned_lines)
                context_parts.append(clean_content[:800])
        
        if not context_parts:
            return "⚠️ Document loaded but no clear answer found. Try a more specific question."
        
        combined_context = "\n\n".join(context_parts)
        
        # Use LLM to generate intelligent answer from context
        from langchain_groq import ChatGroq
        import os
        
        groq_api_key = os.getenv("GROQ_API_KEY")
        if groq_api_key and groq_api_key != "your_groq_api_key_here":
            try:
                llm = ChatGroq(
                    groq_api_key=groq_api_key,
                    model_name="llama-3.1-70b-versatile",
                    temperature=0.2,
                )
                
                prompt = f"""You are a highly intelligent Resume Intelligence System.

<CANDIDATE_DATA>
{combined_context}
</CANDIDATE_DATA>

--- MANDATORY PROCESSING RULES ---
🚫 FORBIDDEN: Copy-pasting sections
🚫 FORBIDDEN: Listing everything you see
🚫 FORBIDDEN: Exceeding 80 words
✅ REQUIRED: Think, analyze, synthesize

**ANALYSIS PHASE:**
Question: "{question}"
What are the 2-3 most relevant facts that answer this?

**SYNTHESIS PHASE:**
Create a professional answer that:
• Focuses on what's MOST important
• Uses intelligent summarization
• Sounds like a recruiter explaining (not a document dump)

**OUTPUT CONSTRAINTS:**
• Maximum 80 words
• Bullet points only if 3+ items
• Professional, concise tone
• If not found → "Not mentioned in the document"

--- YOUR INTELLIGENT SYNTHESIS (MAX 80 WORDS) ---"""
                
                response = llm.invoke(prompt)
                answer = response.content.strip()
                
                return f"""📄 **Answer from Document**

{answer}

---
💡 *Ask specific questions for more details!*"""
            except Exception as e:
                logger.warning(f"LLM generation failed: {e}, returning raw context")
        
        # Fallback: Return raw context if LLM unavailable
        return f"""📄 **Answer from Document**

{combined_context}

---
💡 *Need more details? Ask a follow-up question!*"""
        
    except Exception as e:
        logger.error(f"Document query error: {e}", exc_info=True)
        return f"❌ Error querying document: {str(e)}"


# ============================================================================
# TOOL 3: WEB SEARCH (Google via DuckDuckGo)
# ============================================================================

def web_search_tool(query: str) -> str:
    """
    Search the web using DuckDuckGo with improved error handling and user feedback
    
    Args:
        query: Search query
    
    Returns:
        Formatted search results or appropriate error message
    """
    try:
        from duckduckgo_search import DDGS
        import time
        
        # Add retry logic for rate limiting
        max_retries = 2
        retry_messages = []
        
        for attempt in range(max_retries):
            try:
                ddgs = DDGS(timeout=20)
                results = list(ddgs.text(query, max_results=3))
                
                if not results:
                    return "⚠️ No search results found for your query. Try rephrasing or ask something else."
                
                # If we had to retry, inform the user
                retry_info = ""
                if retry_messages:
                    retry_info = f"ℹ️ *{' '.join(retry_messages)}*\n\n"
                
                formatted_results = f"{retry_info}🔍 **Web Search Results:**\n\n"
                for i, result in enumerate(results, 1):
                    formatted_results += f"**{i}. {result['title']}**\n"
                    formatted_results += f"{result['body'][:200]}...\n"
                    formatted_results += f"🔗 {result['href']}\n\n"
                
                return formatted_results
                
            except Exception as retry_error:
                if "Ratelimit" in str(retry_error) and attempt < max_retries - 1:
                    retry_msg = f"Search service busy, retrying (attempt {attempt + 2}/{max_retries})..."
                    retry_messages.append(retry_msg)
                    logger.warning(f"Rate limited, retrying... (attempt {attempt + 1})")
                    time.sleep(2)
                    continue
                else:
                    raise retry_error
        
        return "⚠️ Web search temporarily unavailable due to high traffic. Please try again in a moment."
        
    except Exception as e:
        logger.error(f"Web search error: {e}")
        # Don't expose technical errors to user
        if "Ratelimit" in str(e):
            return "⚠️ **Search Rate Limit Reached**\n\nThe search service has temporarily limited requests. This usually resolves in 1-2 minutes.\n\n💡 **Meanwhile, you can:**\n- Ask about your uploaded document\n- Check weather information\n- Query or schedule meetings"
        return "⚠️ Unable to perform web search at this time. I can still help with document queries, weather, and meetings."


# ============================================================================
# TOOL 4: DATABASE QUERY (Natural Language → SQL)
# ============================================================================

def query_meetings_tool(query: str) -> str:
    """
    Query meetings database based on natural language
    
    Args:
        query: Natural language query about meetings
    
    Returns:
        Formatted list of meetings
    """
    session = get_sync_session()
    
    try:
        query_lower = query.lower()
        now = datetime.now()
        today = now.date()
        
        # Build query based on natural language patterns
        stmt = select(Meeting)
        
        # Date filters
        if "today" in query_lower:
            stmt = stmt.where(func.date(Meeting.scheduled_date) == today)
        elif "tomorrow" in query_lower:
            tomorrow = today + timedelta(days=1)
            stmt = stmt.where(func.date(Meeting.scheduled_date) == tomorrow)
        elif "next week" in query_lower or "upcoming" in query_lower:
            next_week = today + timedelta(days=7)
            stmt = stmt.where(
                and_(
                    Meeting.scheduled_date >= datetime.now(),
                    Meeting.scheduled_date <= next_week
                )
            )
        elif "this week" in query_lower:
            week_end = today + timedelta(days=7)
            stmt = stmt.where(
                and_(
                    func.date(Meeting.scheduled_date) >= today,
                    func.date(Meeting.scheduled_date) <= week_end
                )
            )
        
        # Type filters
        if "review" in query_lower:
            stmt = stmt.where(Meeting.title.ilike("%review%"))
        elif "team" in query_lower:
            stmt = stmt.where(Meeting.title.ilike("%team%"))
        
        # Order by date
        stmt = stmt.order_by(Meeting.scheduled_date)
        
        # Execute query
        meetings = session.execute(stmt).scalars().all()
        
        if not meetings:
            return "📅 No meetings found matching your criteria."
        
        # Format results
        result = f"📅 Found {len(meetings)} meeting(s):\n\n"
        for meeting in meetings:
            result += f"• **{meeting.title}**\n"
            result += f"  📅 {meeting.scheduled_date.strftime('%Y-%m-%d %H:%M')}\n"
            if meeting.location:
                result += f"  📍 {meeting.location}\n"
            if meeting.description:
                result += f"  📝 {meeting.description}\n"
            if meeting.weather_condition:
                result += f"  🌤️ Weather: {meeting.weather_condition}\n"
            result += "\n"
        
        return result.strip()
        
    except Exception as e:
        logger.error(f"Database query error: {e}", exc_info=True)
        return f"❌ Error querying meetings: {str(e)}"
    finally:
        try:
            session.close()
        except:
            pass


def create_meeting_tool(title: str, scheduled_date: str, location: str = None, 
                       description: str = None, weather_condition: str = None) -> str:
    """
    Create a new meeting in the database
    
    Args:
        title: Meeting title
        scheduled_date: Date and time (ISO format or parseable string)
        location: Meeting location
        description: Meeting description
        weather_condition: Weather condition at meeting time
    
    Returns:
        Success or error message
    """
    session = get_sync_session()
    
    try:
        # Validate inputs
        if not title or not title.strip():
            return "❌ Meeting title is required."
        
        if not scheduled_date or not scheduled_date.strip():
            return "❌ Meeting date is required."
        
        # Parse date with better error handling
        meeting_date = None
        try:
            if "tomorrow" in scheduled_date.lower():
                meeting_date = datetime.now() + timedelta(days=1)
                meeting_date = meeting_date.replace(hour=10, minute=0, second=0, microsecond=0)
            else:
                # Try ISO format first
                try:
                    meeting_date = datetime.fromisoformat(scheduled_date.replace("Z", "+00:00"))
                except:
                    # Try alternative formats
                    from dateutil import parser
                    try:
                        meeting_date = parser.parse(scheduled_date)
                    except:
                        # Default to tomorrow at 10 AM if parsing fails
                        logger.warning(f"Could not parse date '{scheduled_date}', defaulting to tomorrow at 10 AM")
                        meeting_date = datetime.now() + timedelta(days=1)
                        meeting_date = meeting_date.replace(hour=10, minute=0, second=0, microsecond=0)
        except Exception as e:
            logger.error(f"Date parsing error: {e}")
            return f"❌ Invalid date format: {scheduled_date}"
        
        # Check if meeting already exists with same title
        existing = session.execute(
            select(Meeting).where(
                and_(
                    Meeting.title.ilike(title),
                    func.date(Meeting.scheduled_date) == meeting_date.date()
                )
            )
        ).scalar_one_or_none()
        
        if existing:
            return f"⚠️ A meeting with title '{title}' already exists on {meeting_date.date()}."
        
        # Check for time collisions (meetings within 1 hour window)
        collision_window_start = meeting_date - timedelta(hours=1)
        collision_window_end = meeting_date + timedelta(hours=1)
        
        colliding_meetings = session.execute(
            select(Meeting).where(
                and_(
                    Meeting.scheduled_date >= collision_window_start,
                    Meeting.scheduled_date <= collision_window_end
                )
            )
        ).scalars().all()
        
        if colliding_meetings:
            collision_details = "\n".join([
                f"  - {m.title} at {m.scheduled_date.strftime('%H:%M')}"
                for m in colliding_meetings
            ])
            return f"⚠️ Time conflict detected! Existing meetings around that time:\n{collision_details}\n\nPlease choose a different time."
        
        # Create new meeting
        new_meeting = Meeting(
            title=title.strip(),
            scheduled_date=meeting_date,
            location=(location or "TBD").strip(),
            description=(description or "").strip(),
            weather_condition=weather_condition,
            is_weather_dependent=weather_condition is not None
        )
        
        session.add(new_meeting)
        session.commit()
        
        logger.info(f"✅ Meeting created: {title} on {meeting_date}")
        return f"✅ Meeting **'{title}'** successfully scheduled for **{meeting_date.strftime('%Y-%m-%d %H:%M')}**!"
        
    except Exception as e:
        session.rollback()
        logger.error(f"Meeting creation error: {e}", exc_info=True)
        return f"❌ Error creating meeting: {str(e)}"
    finally:
        try:
            session.close()
        except:
            pass


# ============================================================================
# TOOL REGISTRY (for LangChain)
# ============================================================================

weather_tool = Tool(
    name="get_weather",
    func=lambda x: get_weather_tool(x.split("|")[0].strip(), x.split("|")[1].strip() if "|" in x else "today"),
    description="""Get weather information for a location. 
    Input format: 'location|date_query' where date_query is 'today', 'yesterday', or 'tomorrow'.
    Example: 'Chennai|today' or 'London|tomorrow'"""
)

document_query_tool = Tool(
    name="query_document",
    func=query_document_tool,
    description="Query the uploaded document to answer questions. Returns 'NOT_IN_DOCUMENT' if answer not found."
)

search_tool = Tool(
    name="web_search",
    func=web_search_tool,
    description="Search the web for information when the answer is not in the uploaded document."
)

db_query_tool = Tool(
    name="query_meetings",
    func=query_meetings_tool,
    description="Query the meetings database using natural language. Can filter by date (today, tomorrow, next week) or type (review, team)."
)

# Export all tools
all_tools = [weather_tool, document_query_tool, search_tool, db_query_tool]
