#!/bin/bash
# Start script for Render deployment

# Use PORT environment variable from Render, default to 10000 if not set
PORT=${PORT:-10000}

echo "Starting server on port $PORT..."
uvicorn main:app --host 0.0.0.0 --port $PORT

