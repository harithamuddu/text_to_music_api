#!/bin/bash
PORT=${PORT:-10000}
echo "Starting Uvicorn on port $PORT..."
uvicorn main:app --host 0.0.0.0 --port $PORT

