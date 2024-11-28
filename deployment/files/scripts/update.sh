#!/bin/bash

# Step 1: Pull the latest graphchat image
echo "Pulling the latest graphchat image..."
docker pull ryaneggz/graphchat:latest

# Step 2: Stop and remove the current graphchat container
echo "Stopping and removing the existing graphchat container..."
docker stop graphchat
docker rm graphchat

# Step 3: Start the new graphchat container with "always" restart policy
echo "Starting the updated graphchat container with restart policy..."
docker compose up -d --no-deps graphchat

# Step 4: Verify the new container is running
echo "Checking the status of the updated graphchat container..."
docker ps | grep graphchat

echo "Graphchat container has been successfully updated and is set to restart always."
