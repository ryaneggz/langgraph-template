#!/bin/bash

SHORT_SHA=$(git rev-parse --short HEAD)

# Set TAG to first argument if provided, otherwise use SHORT_SHA
TAG=${1:-$SHORT_SHA}

########################################################################
## Container Registry
########################################################################
# Define your GCP parameters
REPOSITORY="ryaneggz"  # Name of your Artifact Registry repository
PROJECT_ID="graphchat"

# Build the Docker image and tag it for Artifact Registry
docker build --squash -t $REPOSITORY/$PROJECT_ID:$TAG .

########################################################################
## Docker Hub
########################################################################
echo ""
## Prompt to push the image to Docker Hub
echo "Do you want to push the image to Docker Hub? (y/n)"
read -r response
if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]
then
  docker push $REPOSITORY/$PROJECT_ID:$TAG
fi
