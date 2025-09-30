#!/bin/bash

# Usage:
# ./initiate           # Start docker-compose
# ./initiate -b        # Build Docker image and start docker-compose
# ./initiate -d        # Stop and remove containers
# ./initiate -r        # Restart containers

set -e

if [[ "$1" == "-b" ]]; then
    echo "Building Docker image and starting containers..."
    docker-compose build
    docker-compose up -d
elif [[ "$1" == "-d" ]]; then
    echo "Stopping and removing containers..."
    docker-compose down
elif [[ "$1" == "-r" ]]; then
    echo "Restarting containers..."
    docker-compose restart
else
    echo "Starting containers..."
    docker-compose up
fi
