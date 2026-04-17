#!/bin/bash

# XYO Container Health Synchronization Script
# Runs container health check and synchronizes with XYO invariants

set -e

CONTAINER_NAMES=(
    "tenetaiagency-101"
    "ultimate-engine"
    "engine-365-days"
    "restricted-aichatbot-trader"
)

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   XYO Container Health Synchronization                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Run Python XYO sync
python3 engine_core/xyo_invariants.py

echo ""
echo "Container Status via Docker:"
echo "────────────────────────────────────────────────────────────"

for container in "${CONTAINER_NAMES[@]}"; do
    if docker ps --filter "name=$container" --quiet | grep -q .; then
        status=$(docker inspect -f '{{.State.Status}}' "$container" 2>/dev/null || echo "unknown")
        health=$(docker inspect -f '{{.State.Health.Status}}' "$container" 2>/dev/null || echo "none")
        
        if [ "$health" = "healthy" ]; then
            echo "✓ $container: $status ($health)"
        elif [ "$health" = "unhealthy" ]; then
            echo "⚠ $container: $status ($health)"
        else
            echo "• $container: $status"
        fi
    else
        echo "✗ $container: not running"
    fi
done

echo ""
echo "────────────────────────────────────────────────────────────"
echo "Synchronization complete."
