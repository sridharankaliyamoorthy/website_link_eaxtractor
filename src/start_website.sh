#!/bin/bash

# Start the Flask API server
echo "Starting Flask API server on http://localhost:5000..."
python3 api.py &
API_PID=$!

# Wait a moment for API to start
sleep 2

# Start a simple HTTP server for the frontend
echo "Starting frontend server on http://localhost:8000..."
echo "Open http://localhost:8000 in your browser"
python3 -m http.server 8000 &
SERVER_PID=$!

# Function to cleanup on exit
cleanup() {
    echo "Stopping servers..."
    kill $API_PID $SERVER_PID 2>/dev/null
    exit
}

# Trap Ctrl+C
trap cleanup INT TERM

# Wait for processes
wait

