"""
Combined Frontend + Backend for Hugging Face Spaces
Runs backend API and frontend on the same service
"""

import os
import subprocess
import time
from multiprocessing import Process

def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting backend on port 8000...")
    subprocess.run([
        "uvicorn", 
        "backend.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])

def start_frontend():
    """Start the Flask frontend"""
    print("🚀 Starting frontend on port 7860...")
    time.sleep(5)  # Wait for backend to start
    os.environ['BACKEND_URL'] = 'http://localhost:8000'
    subprocess.run([
        "python", 
        "-m", 
        "frontend.server"
    ])

if __name__ == '__main__':
    # Start backend in separate process
    backend_process = Process(target=start_backend)
    backend_process.start()
    
    # Start frontend in main process
    start_frontend()
