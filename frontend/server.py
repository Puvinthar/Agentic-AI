"""
Agentic AI Frontend Server - Modern Gemini-like Interface
Flask-based web server with clean, responsive UI
Production-ready with environment configuration
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os
from pathlib import Path
import json

# ============================================================================
# CONFIGURATION
# ============================================================================

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Support both local and production deployment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG_MODE = ENVIRONMENT == "development"

if ENVIRONMENT == "production":
    # Production: backend might be on same host or different domain
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
else:
    # Development: backend on localhost:8000
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

print(f"Environment: {ENVIRONMENT}")
print(f"Backend URL: {BACKEND_URL}")
print(f"Debug Mode: {DEBUG_MODE}")

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/')
def index():
    """Serve the main interface"""
    return render_template('index.html', backend_url=BACKEND_URL)


@app.route('/api/chat', methods=['POST'])
def chat():
    """Proxy chat requests to backend"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message.strip():
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Call backend
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            json={"query": message},
            timeout=60
        )
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'response': response.json().get('response', 'No response')
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Backend error: {response.status_code}'
            }), 500
    
    except requests.Timeout:
        return jsonify({
            'success': False,
            'error': 'Request timeout. Backend server is busy.'
        }), 504
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload file to backend for RAG"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if not file or file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Send to backend with proper file handling
        files = {'file': (file.filename, file.stream, file.content_type)}
        response = requests.post(
            f"{BACKEND_URL}/api/upload",
            files=files,
            timeout=120  # Increased timeout for processing
        )
        
        if response.status_code == 200:
            backend_response = response.json()
            return jsonify({
                'success': True,
                'status': 'success',
                'message': backend_response.get('message', 'File uploaded successfully'),
                'filename': backend_response.get('filename', file.filename)
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Backend returned {response.status_code}: {response.text[:200]}'
            }), 400
    
    except requests.Timeout:
        return jsonify({
            'success': False,
            'error': 'Upload timeout - server took too long to process the file'
        }), 504
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/meetings', methods=['GET'])
def get_meetings():
    """Get meetings from backend"""
    try:
        date_filter = request.args.get('date', 'today')
        
        response = requests.get(
            f"{BACKEND_URL}/api/meetings",
            params={"date": date_filter},
            timeout=30
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Failed to fetch meetings'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/meetings', methods=['POST'])
def create_meeting():
    """Create a new meeting"""
    try:
        data = request.get_json()
        
        response = requests.post(
            f"{BACKEND_URL}/api/meetings",
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return jsonify({'success': True, 'data': response.json()})
        else:
            return jsonify({'success': False, 'error': 'Failed to create meeting'}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Check backend health"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
        if response.status_code == 200:
            return jsonify({'status': 'online', 'healthy': True})
        else:
            return jsonify({'status': 'error', 'healthy': False}), 500
    except:
        return jsonify({'status': 'offline', 'healthy': False}), 503


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print(">> Agentic AI Frontend Server")
    print("="*60)
    print(f"Backend URL: {BACKEND_URL}")
    
    # Get port from environment (HF Spaces uses 7860)
    PORT = int(os.getenv("PORT", 7860))
    
    if ENVIRONMENT == "development":
        print(f"Accessing at: http://localhost:{PORT}")
        print("WARNING: This is a development server")
        print("="*60 + "\n")
        
        app.run(
            host='0.0.0.0',
            port=PORT,
            debug=True,
            use_reloader=False
        )
    else:
        print(f"Production mode - Running on port {PORT}")
        print(f"Command: gunicorn -w 4 -b 0.0.0.0:{PORT} server:app")
        print("="*60 + "\n")
        
        app.run(
            host='0.0.0.0',
            port=PORT,
            debug=False
        )
