#!/bin/bash

# Build script for multi-stage Docker images

echo "Building base image with conda environment..."
docker build -t langchain-base -f Dockerfile.base .

if [ $? -eq 0 ]; then
    echo "Base image built successfully!"
    echo "Building application image using base image..."
    docker build -t langchain-api -f Dockerfile.app .

    if [ $? -eq 0 ]; then
        echo "Application image built successfully!"
        echo "You can now run the containers with:"
        echo "docker-compose up"
    else
        echo "Failed to build application image"
        exit 1
    fi
else
    echo "Failed to build base image"
    exit 1
fi