# Docker Setup Guide

This project provides two different Docker configurations for different use cases:

## Development Setup (docker-compose.dev.yml)

For development with hot-reloading and volume mounting:

```bash
# Build the base image first (run once or when environment.yml changes)
docker build -t langchain-base -f Dockerfile.base .

# Run development environment
docker-compose -f docker-compose.dev.yml up
```

**Features:**
- Uses pre-built `langchain-base` image
- Mounts local code as volumes for live updates
- Faster rebuilds during development
- Ideal for active development

## Production Setup (docker-compose.prod.yml)

For production deployment with fully contained images:

```bash
# Build everything from scratch (no pre-built images needed)
docker-compose -f docker-compose.prod.yml up --build
```

**Features:**
- Builds images from Dockerfile.base and Dockerfile.app
- Fully contained with all code included in images
- No volume mounting
- Ideal for deployment

## Building Images Separately

You can also build images separately for better control:

```bash
# Build base image (when environment.yml changes)
docker build -t langchain-base -f Dockerfile.base .

# Build application image (when code changes)
docker build -t langchain-api -f Dockerfile.app .

# Run with pre-built images
docker-compose -f docker-compose.prod.yml up
```

## File Structure

- `Dockerfile.base` - Base image with conda environment and dependencies
- `Dockerfile.app` - Application image built FROM base image
- `docker-compose.dev.yml` - Development configuration with volume mounting
- `docker-compose.prod.yml` - Production configuration with full builds