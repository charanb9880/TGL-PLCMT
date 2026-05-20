#!/bin/bash
set -e

ENV=$1
echo "🚨 HEALTH CHECK FAILED. INITIATING ROLLBACK FOR $ENV 🚨"

# In a standard docker-compose environment without a registry,
# a rollback involves finding the previous successful image tag or 
# simply reverting the docker-compose state.

echo "Reverting to previous stable state..."
# If using a registry, we would update the .env TAG to the PREVIOUS_TAG and run docker-compose up -d
# For local compose, we can restart the containers from the previous backup if available.

# Assuming PREVIOUS_COMMIT is passed as an env var from Jenkins
if [ -n "$PREVIOUS_COMMIT" ]; then
    echo "Rolling back to commit: $PREVIOUS_COMMIT"
    git checkout $PREVIOUS_COMMIT
    docker-compose -f docker-compose.yml up -d --build
    echo "Rollback complete."
else
    echo "No PREVIOUS_COMMIT provided. Manual intervention required."
    exit 1
fi
