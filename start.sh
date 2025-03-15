#!/bin/bash

# Start the backend
echo "Starting the backend..."
cd "$(dirname "$0")"
source venv/bin/activate
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# Start the frontend
echo "Starting the frontend..."
cd frontend-react
npm start &
FRONTEND_PID=$!

# Function to handle script termination
function cleanup {
  echo "Stopping the backend and frontend..."
  kill $BACKEND_PID
  kill $FRONTEND_PID
  exit
}

# Register the cleanup function for script termination
trap cleanup SIGINT SIGTERM

# Wait for user input to stop the servers
echo "Press Ctrl+C to stop the servers..."
wait 