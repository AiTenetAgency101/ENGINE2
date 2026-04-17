#!/bin/bash
# ENGINE Health Monitoring Script
# Run continuously: docker run -d engine/health-monitor

set -e

SERVICE_CHECK_INTERVAL=300  # 5 minutes
ALERT_THRESHOLD=3
RESTART_ATTEMPTS=3

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "ENGINE Health Monitoring Started"
echo "Checking services every ${SERVICE_CHECK_INTERVAL}s"

while true; do
  TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
  
  echo ""
  echo "[$TIMESTAMP] Running health checks..."
  
  # Check if Docker daemon is running
  if ! docker ps > /dev/null 2>&1; then
    echo -e "${RED}✗ Docker daemon not responding${NC}"
    sleep $SERVICE_CHECK_INTERVAL
    continue
  fi
  
  # Check each ENGINE service
  SERVICES=(
    "tenetaiagency-101:8000"
    "ultimate-engine:3000"
    "engine-365-days:8080"
    "restricted-aichatbot-trader:5000"
  )
  
  FAILED_SERVICES=()
  
  for service in "${SERVICES[@]}"; do
    SERVICE_NAME=$(echo $service | cut -d: -f1)
    SERVICE_PORT=$(echo $service | cut -d: -f2)
    
    # Check if container is running
    if docker ps --format "{{.Names}}" | grep -q "^${SERVICE_NAME}$"; then
      # Check if service is responding on port
      if nc -z localhost $SERVICE_PORT 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $SERVICE_NAME (port $SERVICE_PORT) - HEALTHY"
      else
        echo -e "${RED}✗${NC} $SERVICE_NAME (port $SERVICE_PORT) - NOT RESPONDING"
        FAILED_SERVICES+=("$SERVICE_NAME")
      fi
    else
      echo -e "${RED}✗${NC} $SERVICE_NAME - NOT RUNNING"
      FAILED_SERVICES+=("$SERVICE_NAME")
    fi
  done
  
  # Auto-remediation for failed services
  if [ ${#FAILED_SERVICES[@]} -gt 0 ]; then
    echo -e "${YELLOW}⚠ Found ${#FAILED_SERVICES[@]} failed service(s)${NC}"
    
    for failed_service in "${FAILED_SERVICES[@]}"; do
      echo "Attempting recovery for $failed_service..."
      
      for attempt in $(seq 1 $RESTART_ATTEMPTS); do
        echo "  Restart attempt $attempt/$RESTART_ATTEMPTS..."
        docker-compose -f docker-compose-production.yml restart $failed_service 2>/dev/null || true
        sleep 5
        
        if docker ps --format "{{.Names}}" | grep -q "^${failed_service}$"; then
          echo -e "${GREEN}✓${NC} $failed_service recovered"
          break
        fi
      done
      
      if ! docker ps --format "{{.Names}}" | grep -q "^${failed_service}$"; then
        echo -e "${RED}✗${NC} $failed_service recovery failed - escalating alert"
        # Send alert (Slack, email, etc.)
      fi
    done
  fi
  
  # Check infrastructure services
  echo ""
  echo "Checking infrastructure services..."
  
  INFRA_SERVICES=(
    "engine-postgres:5432"
    "engine-redis:6379"
    "engine-prometheus:9090"
    "engine-grafana:3000"
  )
  
  for service in "${INFRA_SERVICES[@]}"; do
    SERVICE_NAME=$(echo $service | cut -d: -f1)
    SERVICE_PORT=$(echo $service | cut -d: -f2)
    
    if docker ps --format "{{.Names}}" | grep -q "^${SERVICE_NAME}$"; then
      echo -e "${GREEN}✓${NC} $SERVICE_NAME (port $SERVICE_PORT) - RUNNING"
    else
      echo -e "${YELLOW}~${NC} $SERVICE_NAME - QUEUED FOR DEPLOYMENT"
    fi
  done
  
  # System metrics
  echo ""
  echo "System Metrics:"
  
  # Docker stats (no-stream = single output)
  CONTAINER_COUNT=$(docker ps | wc -l)
  echo "  Containers running: $((CONTAINER_COUNT - 1))"
  
  # Disk usage
  DISK_USAGE=$(docker system df --format "table {{.Type}}\t{{.Size}}" 2>/dev/null | tail -1 || echo "N/A")
  echo "  Docker disk usage: $DISK_USAGE"
  
  # Volume count
  VOLUME_COUNT=$(docker volume ls | wc -l)
  echo "  Persistent volumes: $((VOLUME_COUNT - 1))"
  
  echo ""
  echo "Next check in ${SERVICE_CHECK_INTERVAL}s..."
  sleep $SERVICE_CHECK_INTERVAL
done
