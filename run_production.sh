#!/bin/bash
# Production startup script for Agentic AI

# Set environment variables
export ENVIRONMENT=production
export BACKEND_URL=${BACKEND_URL:-"http://localhost:8000"}
export FLASK_ENV=production
export FLASK_DEBUG=0

echo "🚀 Starting Agentic AI Frontend (Production)"
echo "📡 Backend URL: $BACKEND_URL"
echo "🌐 Listening on 0.0.0.0:5000"

# Run with Gunicorn (4 workers, suitable for most deployments)
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 60 --access-logfile - server:app
