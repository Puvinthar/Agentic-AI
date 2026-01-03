#!/bin/bash

# Start backend in background
echo "Starting backend..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Wait for backend to start
sleep 5

# Start frontend
echo "Starting frontend..."
python -m frontend.server
