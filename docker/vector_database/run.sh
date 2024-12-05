#!/bin/bash

PORT=6333  # Replace with the port you want to clean up

echo "Cleaning up processes using port $PORT..."

# Find processes using the port and kill them
PID=$(sudo lsof -t -i:$PORT)
if [ -n "$PID" ]; then
    echo "Found process with PID $PID on port $PORT. Killing process..."
    sudo kill -9 $PID
    echo "Process on port $PORT terminated."
else
    echo "No process found using port $PORT."
fi

echo "Starting Docker Compose..."
# Run Docker Compose
docker compose up -d
