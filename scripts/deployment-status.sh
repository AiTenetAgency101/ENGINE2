#!/bin/bash
# ENGINE Production Status Report
# Generated: 2026-04-15 02:30 UTC

echo "=============================================="
echo "ENGINE v1.0.0 - PRODUCTION DEPLOYMENT STATUS"
echo "=============================================="
echo ""

# Container Status
echo "## RUNNING SERVICES (Active)"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Image}}" --filter "status=running" | head -10

echo ""
echo "## SERVICE HEALTH CHECK"
echo ""

# Core Services Health
services=(
  "tenetaiagency-101:8000"
  "ultimate-engine:3000"
  "engine-365-days:8080"
  "restricted-aichatbot-trader:5000"
)

for service in "${services[@]}"; do
  name=$(echo $service | cut -d: -f1)
  port=$(echo $service | cut -d: -f2)
  
  if docker ps | grep -q "$name"; then
    echo "✓ $name (port $port) - RUNNING"
  else
    echo "✗ $name - NOT RUNNING"
  fi
done

echo ""
echo "## INFRASTRUCTURE SERVICES STATUS"
echo ""

# Check volumes
echo "Data Volumes:"
docker volume ls --filter "name=engine" --format "{{.Name}}" | wc -l

echo ""
echo "## API ENDPOINTS (When ready)"
echo ""
echo "EHF Performance Dashboard:"
echo "  http://localhost:9001/api/ehf/status"
echo ""
echo "Smart Home Control:"
echo "  http://localhost:9000/api/zha/devices"
echo ""
echo "System Health:"
echo "  http://localhost:9000/api/tron/status"
echo ""
echo "Prometheus Metrics:"
echo "  http://localhost:9090"
echo ""
echo "Grafana Dashboards:"
echo "  http://localhost:3000"
echo ""
echo "Jaeger Tracing:"
echo "  http://localhost:16686"
echo ""
echo "AlertManager:"
echo "  http://localhost:9093"
echo ""

echo "=============================================="
echo "GIT REPOSITORY STATUS"
echo "=============================================="
echo ""
cd /Users/ENGINE 2>/dev/null || cd C:/Users/ENGINE
git log --oneline -3
echo ""
git remote -v
echo ""

echo "=============================================="
echo "DEPLOYMENT COMPLETE"
echo "=============================================="
