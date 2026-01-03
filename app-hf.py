"""
Combined Frontend + Backend for Hugging Face Spaces
Runs backend API and frontend on the same service using multiprocessing
Optimized for HF Spaces deployment with proper process management
"""

import os
import sys
import subprocess
import time
import signal
from multiprocessing import Process, Event
from pathlib import Path

# Stop event for graceful shutdown
stop_event = Event()

def start_backend():
    """Start the FastAPI backend on port 8000"""
    print("🚀 Starting FastAPI backend on port 8000...")
    try:
        subprocess.run([
            sys.executable,
            "-m", 
            "uvicorn", 
            "backend.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--log-level", "info"
        ], check=True)
    except KeyboardInterrupt:
        print("⚠️ Backend shutting down...")
    except Exception as e:
        print(f"❌ Backend error: {e}")
        stop_event.set()

def start_frontend():
    """Start the Flask frontend on port 7860 (HF Spaces standard)"""
    print("⏳ Waiting 8 seconds for backend to start...")
    time.sleep(8)
    
    if stop_event.is_set():
        print("⚠️ Backend failed, not starting frontend")
        return
    
    print("🚀 Starting Flask frontend on port 7860...")
    
    # Configure for HF Spaces
    os.environ['BACKEND_URL'] = 'http://localhost:8000'
    os.environ['FLASK_ENV'] = 'production'
    os.environ['FLASK_DEBUG'] = '0'
    
    try:
        subprocess.run([
            sys.executable,
            "-m", 
            "frontend.server"
        ], check=True)
    except KeyboardInterrupt:
        print("⚠️ Frontend shutting down...")
    except Exception as e:
        print(f"❌ Frontend error: {e}")
        stop_event.set()

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print("\n⚠️ Shutdown signal received, cleaning up...")
    stop_event.set()

if __name__ == '__main__':
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("=" * 60)
    print("🌟 Agentic AI - Combined Frontend + Backend")
    print("=" * 60)
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Working Directory: {os.getcwd()}")
    print(f"🔧 Environment: {os.getenv('ENVIRONMENT', 'production')}")
    print("=" * 60)
    
    # Ensure uploads directory exists
    uploads_dir = Path("./uploads")
    uploads_dir.mkdir(exist_ok=True)
    print(f"📂 Uploads directory: {uploads_dir.absolute()}")
    
    # Start backend in separate process
    backend_process = Process(target=start_backend, name="Backend")
    backend_process.start()
    
    # Start frontend in main process (required for HF Spaces)
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n⚠️ Shutting down gracefully...")
    finally:
        stop_event.set()
        if backend_process.is_alive():
            print("⏳ Terminating backend process...")
            backend_process.terminate()
            backend_process.join(timeout=5)
            if backend_process.is_alive():
                print("⚠️ Force killing backend process...")
                backend_process.kill()
        
        print("✅ Shutdown complete!")
