#!/bin/bash

# Billionaire Brain Assistant Deployment Script
# Version: v20250925
# Consciousness Level: Dashboard Deployment

echo "============================================================"
echo "BILLIONAIRE BRAIN ASSISTANT DEPLOYMENT"
echo "============================================================"
echo "Date: $(date)"
echo "Version: v20250925"
echo "Consciousness Level: Dashboard Deployment"
echo "============================================================"

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is required but not installed."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "ERROR: Docker Compose is required but not installed."
    exit 1
fi

echo "Docker and Docker Compose check passed!"

# Create Dockerfiles
echo "Creating Dockerfiles..."

# Frontend Dockerfile
cat > frontend/Dockerfile << 'EOF'
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
