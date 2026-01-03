"""
FastAPI Application - Agentic AI Backend
Main entry point with all API endpoints
"""
import os
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import init_db, get_async_session, test_connection
from backend.agents import process_query_sync
from backend.tools import load_document_tool
from backend.models import Meeting, DocumentMetadata

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create uploads directory
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Track if document is loaded
document_loaded = False
current_document_path = None


# ============================================================================
# LIFESPAN CONTEXT (Database Initialization)
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    logger.info("🚀 Starting Agentic AI Backend...")
    
    # Test database connection with timeout (non-blocking)
    try:
        db_connected = await test_connection()
        
        if db_connected:
            # Initialize database tables
            await init_db()
            logger.info("✅ Database initialized successfully")
        else:
            logger.warning("⚠️ Starting without database. Meeting scheduler features will be unavailable.")
    except Exception as e:
        logger.warning(f"⚠️ Database initialization failed: {e}. App starting without database features.")
    
    logger.info("✅ Backend API is ready!")
    
    yield
    
    logger.info("👋 Shutting down Agentic AI Backend...")


# ============================================================================
# FASTAPI APP INITIALIZATION
# ============================================================================

app = FastAPI(
    title="Agentic AI Backend",
    description="Intelligent AI agent system with weather, document RAG, web search, and database capabilities",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class ChatRequest(BaseModel):
    """Chat request model"""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "query": "What is the weather in Chennai today?"
        }
    })
    query: str = Field(..., description="User's question or command")


class ChatResponse(BaseModel):
    """Chat response model"""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "response": "The weather in Chennai today is sunny with a temperature of 32°C.",
            "timestamp": "2026-01-01T10:30:00"
        }
    })
    response: str = Field(..., description="AI agent's response")
    timestamp: str = Field(..., description="Response timestamp")


class MeetingCreate(BaseModel):
    """Meeting creation model"""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "title": "Team Standup",
            "scheduled_date": "2026-01-02T10:00:00",
            "location": "Conference Room A",
            "description": "Daily team sync"
        }
    })
    title: str = Field(..., description="Meeting title")
    scheduled_date: str = Field(..., description="Scheduled date/time (ISO format or 'tomorrow')")
    location: Optional[str] = Field(None, description="Meeting location")
    description: Optional[str] = Field(None, description="Meeting description")


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🤖 Agentic AI Backend is running!",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "upload": "/api/upload",
            "meetings": "/api/meetings",
            "health": "/api/health"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    db_status = await test_connection()
    
    return {
        "status": "healthy" if db_status else "degraded",
        "database": "connected" if db_status else "disconnected",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - processes user queries through the agentic workflow
    
    **Agent Capabilities:**
    - 🌤️ Weather queries (Agent 1)
    - 📄 Document Q&A with web fallback (Agent 2)
    - 📅 Meeting scheduling with weather reasoning (Agent 3)
    - 🗄️ Natural language database queries (Agent 4)
    
    **Examples:**
    - "What is the weather in Chennai today?"
    - "What is the leave policy?" (requires uploaded document)
    - "Schedule a team meeting if weather is good tomorrow"
    - "Show all meetings scheduled tomorrow"
    """
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        logger.info(f"📨 Received query: {request.query}")
        
        # Process query through agentic workflow (synchronous wrapper)
        import asyncio
        response = await asyncio.to_thread(
            lambda: process_query_sync(request.query, document_loaded)
        )
        
        if not response:
            response = "Sorry, I couldn't generate a response. Please try again."
        
        return ChatResponse(
            response=response,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")


@app.post("/api/upload")
async def upload_document(
    file: UploadFile = File(..., description="PDF or TXT document to upload"),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Upload and process a document for RAG (Retrieval Augmented Generation)
    
    **Supported formats:** PDF, TXT
    
    Once uploaded, you can ask questions about the document content.
    If the answer is not in the document, the agent will search the web.
    """
    global document_loaded, current_document_path
    
    try:
        # Validate file
        if not file or not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Validate file type
        allowed_extensions = [".pdf", ".txt"]
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type '{file_ext}'. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Read and save file
        try:
            content = await file.read()
            if not content:
                raise HTTPException(status_code=400, detail="File is empty")
            
            file_path = UPLOAD_DIR / file.filename
            with open(file_path, "wb") as f:
                f.write(content)
            
            logger.info(f"📁 File saved: {file_path}")
        except Exception as e:
            logger.error(f"Error saving file: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
        
        # Mark document as loaded immediately and start processing in background
        document_loaded = True
        current_document_path = str(file_path)
        
        # Save metadata to database (async)
        try:
            doc_metadata = DocumentMetadata(
                filename=file.filename,
                filepath=str(file_path),
                file_type=file_ext,
                processed=True
            )
            session.add(doc_metadata)
            await session.commit()
            logger.info(f"✅ Document metadata saved: {file.filename}")
        except Exception as e:
            logger.warning(f"Failed to save document metadata: {e}")
            await session.rollback()
        
        # Process document in background thread (non-blocking)
        import asyncio
        import threading
        
        def process_in_background():
            try:
                result = load_document_tool(str(file_path))
                logger.info(f"Document processing result: {result}")
            except Exception as e:
                logger.error(f"Background document processing error: {e}", exc_info=True)
        
        # Start background processing
        thread = threading.Thread(target=process_in_background, daemon=True)
        thread.start()
        
        return {
            "status": "success",
            "message": f"✅ Document '{file.filename}' uploaded successfully! Processing in background...",
            "filename": file.filename,
            "file_size_bytes": len(content),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.get("/api/meetings")
async def get_meetings(
    date: Optional[str] = None,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get all meetings (optionally filtered by date)
    
    **Query Parameters:**
    - date: ISO format date (e.g., 2026-01-02) or keywords like 'today', 'tomorrow'
    """
    try:
        # Ensure database is reachable before proceeding
        db_ok = await test_connection()
        if not db_ok:
            raise HTTPException(
                status_code=503,
                detail="Database unavailable. Verify DATABASE_URL/SYNC_DATABASE_URL and PostgreSQL credentials."
            )

        from sqlalchemy import select, func
        from datetime import timedelta
        
        stmt = select(Meeting)
        
        if date:
            date_lower = date.lower()
            today = datetime.now().date()
            
            if date_lower == "today":
                stmt = stmt.where(func.date(Meeting.scheduled_date) == today)
            elif date_lower == "tomorrow":
                tomorrow = today + timedelta(days=1)
                stmt = stmt.where(func.date(Meeting.scheduled_date) == tomorrow)
            else:
                try:
                    target_date = datetime.fromisoformat(date).date()
                    stmt = stmt.where(func.date(Meeting.scheduled_date) == target_date)
                except ValueError:
                    raise HTTPException(status_code=400, detail="Invalid date format")
        
        stmt = stmt.order_by(Meeting.scheduled_date)
        
        result = await session.execute(stmt)
        meetings = result.scalars().all()
        
        return {
            "count": len(meetings),
            "meetings": [meeting.to_dict() for meeting in meetings]
        }
        
    except Exception as e:
        logger.error(f"Error fetching meetings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/meetings")
async def create_meeting_endpoint(
    meeting: MeetingCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new meeting
    
    **Request Body:**
    ```json
    {
        "title": "Team Meeting",
        "scheduled_date": "2026-01-02T10:00:00",
        "location": "Conference Room",
        "description": "Weekly sync"
    }
    ```
    """
    try:
        # Ensure database is reachable before proceeding
        db_ok = await test_connection()
        if not db_ok:
            raise HTTPException(
                status_code=503,
                detail="Database unavailable. Verify DATABASE_URL/SYNC_DATABASE_URL and PostgreSQL credentials."
            )

        from backend.tools import create_meeting_tool
        
        result = create_meeting_tool(
            title=meeting.title,
            scheduled_date=meeting.scheduled_date,
            location=meeting.location,
            description=meeting.description
        )
        
        if "successfully" in result.lower():
            return {
                "status": "success",
                "message": result,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "warning",
                "message": result,
                "timestamp": datetime.now().isoformat()
            }
        
    except Exception as e:
        logger.error(f"Error creating meeting: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/meetings/{meeting_id}")
async def delete_meeting(
    meeting_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Delete a meeting by ID"""
    try:
        from sqlalchemy import select
        
        stmt = select(Meeting).where(Meeting.id == meeting_id)
        result = await session.execute(stmt)
        meeting = result.scalar_one_or_none()
        
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")
        
        await session.delete(meeting)
        await session.commit()
        
        return {
            "status": "success",
            "message": f"Meeting '{meeting.title}' deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting meeting: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/document/status")
async def document_status():
    """Get current document status"""
    return {
        "document_loaded": document_loaded,
        "current_document": current_document_path,
        "timestamp": datetime.now().isoformat()
    }


@app.delete("/api/document")
async def clear_document():
    """Clear the currently loaded document"""
    global document_loaded, current_document_path
    
    document_loaded = False
    current_document_path = None
    
    return {
        "status": "success",
        "message": "Document cleared successfully"
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
