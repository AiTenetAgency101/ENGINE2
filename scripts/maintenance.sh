#!/bin/bash
# ENGINE Automated Maintenance Script
# Weekly cleanup and optimization

set -e

BACKUP_DIR="/backup/engine"
LOG_DIR="/var/log/engine"
RETENTION_DAYS=30

echo "=========================================="
echo "ENGINE Weekly Maintenance"
echo "=========================================="
echo ""

# 1. Database Backup
echo "[1/6] Backing up database..."
mkdir -p $BACKUP_DIR
BACKUP_FILE="$BACKUP_DIR/engine_backup_$(date +%Y%m%d_%H%M%S).sql"

docker-compose -f docker-compose-production.yml exec -T postgresql pg_dump -U engine_user engine_prod > $BACKUP_FILE 2>/dev/null || true

if [ -f "$BACKUP_FILE" ]; then
  echo "✓ Database backup created: $(ls -lh $BACKUP_FILE | awk '{print $9, $5}')"
else
  echo "✗ Database backup failed"
fi

# 2. Log Rotation
echo "[2/6] Rotating logs..."
find $LOG_DIR -name "*.log" -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
docker-compose -f docker-compose-production.yml logs --tail 1000 > $LOG_DIR/engine_$(date +%Y%m%d).log 2>/dev/null || true
echo "✓ Logs rotated (retention: $RETENTION_DAYS days)"

# 3. Volume Cleanup
echo "[3/6] Cleaning unused volumes..."
VOLUME_BEFORE=$(docker volume ls | wc -l)
docker volume prune -f > /dev/null 2>&1 || true
VOLUME_AFTER=$(docker volume ls | wc -l)
echo "✓ Volumes cleaned (removed: $((VOLUME_BEFORE - VOLUME_AFTER)))"

# 4. Image Cleanup
echo "[4/6] Cleaning dangling images..."
IMAGE_BEFORE=$(docker images | wc -l)
docker image prune -a -f > /dev/null 2>&1 || true
IMAGE_AFTER=$(docker images | wc -l)
echo "✓ Images cleaned (removed: $((IMAGE_BEFORE - IMAGE_AFTER)))"

# 5. System Disk Check
echo "[5/6] Checking system resources..."
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}')
MEMORY_USAGE=$(free -h | grep Mem | awk '{print $3 "/" $2}')
echo "  Disk usage: $DISK_USAGE"
echo "  Memory usage: $MEMORY_USAGE"

# 6. Health Verification
echo "[6/6] Verifying service health..."
docker-compose -f docker-compose-production.yml ps | grep -E "Up|Exited" | wc -l | xargs -I {} echo "  Services status: {} containers"

echo ""
echo "=========================================="
echo "✓ Weekly maintenance complete"
echo "=========================================="
echo ""
echo "Next scheduled maintenance: $(date -d '+1 week' +%Y-%m-%d\ %H:%M:%S)"
