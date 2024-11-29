#!/bin/bash

ORIGIN=langgraph-template

# Prompt for tag and message
read -p "Enter tag (e.g. 0.0.1-rc1): " tag
read -p "Enter message (press enter for none): " message

# Show details and confirm
echo -e "\nTag details:"
echo "Tag: $tag"
echo "Message: ${message:-<empty>}"

read -p "Proceed with creating and pushing tag? (y/N) " confirm

if [[ $confirm =~ ^[Yy]$ ]]; then
    if [ -z "$message" ]; then
        git tag -a "$tag" -m ""
    else
        git tag -a "$tag" -m "$message"
    fi
    
    git push $ORIGIN "$tag"
    echo "Tag created and pushed successfully"
else
    echo "Operation cancelled"
fi
