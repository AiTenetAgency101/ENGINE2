#!/bin/bash
# Start full stack locally with Docker Compose

set -e

echo "🚀 Starting ENGINE v1.0.0 full stack..."
echo ""

# Check Docker daemon
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker daemon not running"
    exit 1
fi

# Set Kaggle API key
if [ -z "$KAGGLE_KEY" ]; then
    echo "⚠️  KAGGLE_KEY environment variable not set"
    export KAGGLE_KEY="KGAT_bb4030a949969eca4009e86b404ea4cb"
fi

# Build images
echo "📦 Building images..."
docker compose -f docker-compose-full-stack.yml build --no-cache

# Start services
echo "🔄 Starting services..."
docker compose -f docker-compose-full-stack.yml up -d

echo ""
echo "✅ Services started!"
echo ""
echo "Container Status:"
docker compose -f docker-compose-full-stack.yml ps
echo ""
echo "Engine URLs:"
echo "  - engine-365-days: http://localhost:3000"
echo "  - ultimate-engine: http://localhost:3001"
echo "  - tenetaiagency-101: http://localhost:3002"
echo ""
echo "Logs:"
echo "  docker compose -f docker-compose-full-stack.yml logs -f"
echo ""
echo "Stop stack:"
echo "  docker compose -f docker-compose-full-stack.yml down"
