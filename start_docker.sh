#!/bin/bash

# Define the container name
CONTAINER_NAME="safeqr-ml"
IMAGE_NAME="safeqr-fastapi-app"
PORT_MAPPING="8000:8000"

# Check if the container is running
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping the running Docker container: $CONTAINER_NAME"
    # Stop the container
    docker stop $CONTAINER_NAME
fi

# Check if the container exists (but not running)
if [ "$(docker ps -a -q -f name=$CONTAINER_NAME)" ]; then
    echo "Removing the Docker container: $CONTAINER_NAME"
    # Remove the container
    docker rm $CONTAINER_NAME
fi

# Run the Docker container
echo "Starting a new Docker container: $CONTAINER_NAME"
docker run -d --name $CONTAINER_NAME -p $PORT_MAPPING $IMAGE_NAME

# Print the status of the new container
docker ps -f name=$CONTAINER_NAME
