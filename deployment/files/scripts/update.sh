#!/bin/bash

# Step 1: Set the image tag (default to "latest" if not provided)
IMAGE_TAG=${1:-latest}
IMAGE_NAME="ryaneggz/graphchat:$IMAGE_TAG"

echo "Using image: $IMAGE_NAME"

# Step 2: Pull the specified image tag
echo "Pulling the specified image..."
docker pull $IMAGE_NAME

# Step 3: Stop and remove the current graphchat container
echo "Stopping and removing the existing graphchat container..."
docker stop graphchat
docker rm graphchat

# Step 4: Update the docker-compose file (optional if not using tag directly)
echo "Updating graphchat service to use $IMAGE_NAME in docker-compose..."
sed -i "s|image: ryaneggz/graphchat:.*|image: $IMAGE_NAME|" docker-compose.yml

# Step 5: Start the new graphchat container with "always" restart policy
echo "Starting the updated graphchat container..."
docker compose up -d --no-deps graphchat

# Step 6: Verify the new container is running
echo "Checking the status of the updated graphchat container..."
docker ps | grep graphchat

echo "Graphchat container has been successfully updated and is set to restart always."
