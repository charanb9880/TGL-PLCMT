#!/bin/bash
set -e

ENV=$1
TAG=$2

echo "Starting Deployment to ${ENV} environment..."
echo "Target Tag: ${TAG}"

# Define the environment-specific variables
if [ "$ENV" == "production" ]; then
    PORT_PREFIX="80"
elif [ "$ENV" == "staging" ]; then
    PORT_PREFIX="81"
else
    echo "Unknown environment: $ENV"
    exit 1
fi

# We are using docker-compose. In a real cluster this might be helm or kubectl.
# We will pull the images and restart the services safely.

echo "Pulling latest images..."
docker-compose pull

echo "Starting zero-downtime deployment (recreate)..."
# Using up -d will recreate containers whose images have changed
docker-compose -f docker-compose.yml up -d --build --no-deps

echo "Deployment scripts executed successfully."
exit 0
