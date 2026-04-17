#!/usr/bin/env bash
set -e

echo "=== ENGINE2 CONTAINER HEALTH CHECK ==="
echo "Docker version:"
docker --version

echo "Checking Python inside container..."
docker run --rm ghcr.io/${{ github.repository }}/engine2:latest python3 --version || echo "Python check failed"

echo "Checking engine startup..."
docker run --rm ghcr.io/${{ github.repository }}/engine2:latest python3 /app/main.py || echo "Engine startup failed"

echo "=== HEALTH CHECK COMPLETE ==="
