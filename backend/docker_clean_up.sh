#!/bin/bash

set -e  # Exit immediately on any error

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Check for required commands
if ! command_exists docker; then
    echo "Error: Docker is not installed or not in PATH."
    exit 1
fi

if ! command_exists lsof; then
    echo "Error: 'lsof' command is not installed. Install it to proceed."
    exit 1
fi

echo "Stop and remove all containers and volumes..."
docker compose down --volumes --remove-orphans || true

# Remove all containers (check first to avoid errors)
CONTAINERS=$(docker ps -aq)
if [ -n "$CONTAINERS" ]; then
    echo "Removing all containers..."
    docker rm -vf $CONTAINERS
else
    echo "No containers to remove."
fi

# Remove all volumes (check first to avoid errors)
VOLUMES=$(docker volume ls -q)
if [ -n "$VOLUMES" ]; then
    echo "Removing all volumes..."
    docker volume rm $VOLUMES
else
    echo "No volumes to remove."
fi

echo "Delete all Docker images..."
IMAGES=$(docker images -q)
if [ -n "$IMAGES" ]; then
    docker rmi -f $IMAGES
else
    echo "No Docker images to delete."
fi

echo "Remove all unused Docker networks..."
docker network prune --force

# Clean up processes using a specific port
PORT=6333  # Replace with the port you want to clean up
echo "Cleaning up processes using port $PORT..."
PID=$(sudo lsof -t -i:$PORT)
if [ -n "$PID" ]; then
    echo "Found process with PID $PID on port $PORT. Killing process..."
    sudo kill -9 $PID
    echo "Process on port $PORT terminated."
else
    echo "No process found using port $PORT."
fi

echo "Remove Docker system-wide data..."
docker system prune --all --volumes --force
echo "Docker cleanup completed successfully."
