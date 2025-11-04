#!/bin/bash
port=${PORT:-8000}
echo "Starting Uvicorn on port $port..."
uvicorn main:app --host 0.0.0.0 --port $port
