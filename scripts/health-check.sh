#!/bin/bash
# Production health check & monitoring script

set -euo pipefail

SERVICES=("tenetaiagency-101:8000" "ultimate-engine:3000" "engine-365-days:8080" "restricted-aichatbot-trader:5000")
TIMEOUT=10
RETRIES=3

echo "=========================================="
echo "ENGINE Production Health Check"
echo "=========================================="
echo "Timestamp: $(date)"
echo ""

# Function to check service health
check_service() {
    local service=$1
    local port=$2
    local attempt=1
    
    while [ $attempt -le $RETRIES ]; do
        if curl -sf --max-time $TIMEOUT "http://localhost:$port/health" > /dev/null 2>&1; then
            echo "✅ $service ($port) - HEALTHY"
            return 0
        fi
        echo "⚠️  $service ($port) - Attempt $attempt/$RETRIES failed, retrying..."
        attempt=$((attempt + 1))
        sleep 2
    done
    
    echo "❌ $service ($port) - UNHEALTHY (failed $RETRIES attempts)"
    return 1
}

# Check all services
failed=0
for service in "${SERVICES[@]}"; do
    IFS=':' read -r name port <<< "$service"
    if ! check_service "$name" "$port"; then
        failed=$((failed + 1))
    fi
done

echo ""
echo "=========================================="
echo "Infrastructure Services"
echo "=========================================="

# Check PostgreSQL
if nc -z localhost 5432 > /dev/null 2>&1; then
    echo "✅ PostgreSQL (5432) - ONLINE"
else
    echo "❌ PostgreSQL (5432) - OFFLINE"
    failed=$((failed + 1))
fi

# Check Redis
if redis-cli -p 6379 ping > /dev/null 2>&1; then
    echo "✅ Redis (6379) - ONLINE"
    REDIS_MEMORY=$(redis-cli -p 6379 INFO memory | grep used_memory_human | cut -d: -f2 | tr -d '\r')
    echo "   Memory: $REDIS_MEMORY"
else
    echo "❌ Redis (6379) - OFFLINE"
    failed=$((failed + 1))
fi

# Check Vault
if curl -sf --max-time $TIMEOUT "http://localhost:8200/v1/sys/health" > /dev/null 2>&1; then
    echo "✅ Vault (8200) - ONLINE"
else
    echo "❌ Vault (8200) - OFFLINE"
    failed=$((failed + 1))
fi

echo ""
echo "=========================================="
echo "Monitoring Stack"
echo "=========================================="

# Check Prometheus
if curl -sf --max-time $TIMEOUT "http://localhost:9090/-/healthy" > /dev/null 2>&1; then
    echo "✅ Prometheus (9090) - ONLINE"
else
    echo "❌ Prometheus (9090) - OFFLINE"
fi

# Check Grafana
if curl -sf --max-time $TIMEOUT "http://localhost:3000/api/health" > /dev/null 2>&1; then
    echo "✅ Grafana (3000) - ONLINE"
else
    echo "❌ Grafana (3000) - OFFLINE"
fi

# Check Jaeger
if curl -sf --max-time $TIMEOUT "http://localhost:16686" > /dev/null 2>&1; then
    echo "✅ Jaeger (16686) - ONLINE"
else
    echo "❌ Jaeger (16686) - OFFLINE"
fi

# Check AlertManager
if curl -sf --max-time $TIMEOUT "http://localhost:9093/-/healthy" > /dev/null 2>&1; then
    echo "✅ AlertManager (9093) - ONLINE"
else
    echo "❌ AlertManager (9093) - OFFLINE"
fi

echo ""
echo "=========================================="
echo "System Resources"
echo "=========================================="

if command -v docker &> /dev/null; then
    echo "Docker Disk Usage:"
    docker system df
    echo ""
fi

echo "=========================================="
if [ $failed -eq 0 ]; then
    echo "✅ ALL SYSTEMS HEALTHY"
    exit 0
else
    echo "❌ $failed SERVICE(S) UNHEALTHY"
    exit 1
fi
