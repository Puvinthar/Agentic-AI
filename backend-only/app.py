"""
Backend API Only - Standalone Deployment
Exposes FastAPI with Swagger UI at /docs
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.main import app

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment (for cloud platforms) or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    print("=" * 50)
    print("🚀 Backend API Server Starting")
    print("=" * 50)
    print(f"📡 API Server: http://0.0.0.0:{port}")
    print(f"📚 Swagger UI: http://0.0.0.0:{port}/docs")
    print(f"📖 ReDoc: http://0.0.0.0:{port}/redoc")
    print("=" * 50)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
