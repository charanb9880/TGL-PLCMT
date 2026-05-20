#!/bin/bash
set -e

ENV=$1
echo "Starting health check for $ENV environment..."

# In a real environment, you'd check the actual domain names.
# Here we check the localhost ports mapped in docker-compose.
BACKEND_URL="http://localhost:8000/api/"
FRONTEND_URL="http://localhost:3000/"
AGENT_URL="http://localhost:8001/docs"

check_endpoint() {
    URL=$1
    echo "Checking $URL..."
    HTTP_STATUS=$(curl -o /dev/null -s -w "%{http_code}\n" "$URL")
    
    # We accept 200, 301, 302, 404 (for root API if no route), as long as it's not 500+
    if [ "$HTTP_STATUS" -ge 200 ] && [ "$HTTP_STATUS" -lt 500 ]; then
        echo "✅ $URL is healthy (Status: $HTTP_STATUS)"
    else
        echo "❌ $URL is unhealthy (Status: $HTTP_STATUS)"
        exit 1
    fi
}

# Wait for containers to fully boot
echo "Waiting 15 seconds for services to boot..."
sleep 15

check_endpoint $BACKEND_URL
check_endpoint $AGENT_URL
check_endpoint $FRONTEND_URL

echo "All health checks passed!"
exit 0
