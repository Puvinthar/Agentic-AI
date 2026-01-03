"""
Agentic AI Frontend - Entry Point for Hugging Face Spaces
Wraps Flask app to run on HF Spaces (port 7860)
"""

import os
import sys

# Add frontend to path
sys.path.insert(0, './frontend')

from frontend.server import app

if __name__ == '__main__':
    # HF Spaces runs on port 7860
    port = int(os.getenv('PORT', 7860))
    host = '0.0.0.0'
    
    print(f"\n{'='*60}")
    print(f">> Agentic AI Frontend on HF Spaces")
    print(f"{'='*60}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Backend URL: {os.getenv('BACKEND_URL', 'Not set')}")
    print(f"{'='*60}\n")
    
    app.run(host=host, port=port, debug=False)
