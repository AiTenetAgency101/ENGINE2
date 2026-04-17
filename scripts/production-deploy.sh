#!/bin/bash
# Production deployment script with rollback capability

set -euo pipefail

ENVIRONMENT="${1:-production}"
ACTION="${2:-deploy}"
DRY_RUN="${3:-false}"

echo "=========================================="
echo "ENGINE Production Deployment"
echo "=========================================="
echo "Environment: $ENVIRONMENT"
echo "Action: $ACTION"
echo "Dry Run: $DRY_RUN"
echo "Timestamp: $(date)"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to log
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Validation
if [ ! -f "docker-compose-production.yml" ]; then
    log_error "docker-compose-production.yml not found"
    exit 1
fi

if [ ! -f ".env.production" ]; then
    log_error ".env.production not found"
    exit 1
fi

# Load environment
source .env.production

case $ACTION in
    deploy)
        log_info "Starting deployment..."
        
        # Create data directories
        log_info "Creating data directories..."
        mkdir -p data/{postgres,redis,prometheus,grafana,alertmanager,jaeger,vault,pushgateway}
        
        # Pull latest images
        log_info "Pulling latest images..."
        if [ "$DRY_RUN" != "true" ]; then
            docker-compose -f docker-compose-production.yml pull || log_warn "Some images not available in registry"
        fi
        
        # Build images
        log_info "Building Docker images..."
        if [ "$DRY_RUN" != "true" ]; then
            docker-compose -f docker-compose-production.yml build \
                tenetaiagency-101 \
                ultimate-engine \
                engine-365-days \
                restricted-aichatbot-trader
        fi
        
        # Start containers
        log_info "Starting services..."
        if [ "$DRY_RUN" = "true" ]; then
            log_info "DRY RUN: Would execute:"
            echo "docker-compose -f docker-compose-production.yml up -d"
        else
            docker-compose -f docker-compose-production.yml up -d
            
            # Wait for services to start
            log_info "Waiting for services to start..."
            sleep 10
            
            # Health checks
            log_info "Verifying service health..."
            max_attempts=30
            attempt=0
            
            while [ $attempt -lt $max_attempts ]; do
                healthy=true
                
                for service in tenetaiagency-101 ultimate-engine engine-365-days restricted-aichatbot-trader; do
                    if ! docker-compose -f docker-compose-production.yml ps $service | grep -q "healthy"; then
                        healthy=false
                        break
                    fi
                done
                
                if [ "$healthy" = true ]; then
                    log_info "✅ All services healthy"
                    break
                fi
                
                attempt=$((attempt + 1))
                if [ $attempt -lt $max_attempts ]; then
                    log_warn "Services not healthy yet (attempt $attempt/$max_attempts)..."
                    sleep 10
                fi
            done
            
            if [ $attempt -eq $max_attempts ]; then
                log_error "Services failed to start"
                docker-compose -f docker-compose-production.yml logs
                exit 1
            fi
        fi
        
        log_info "✅ Deployment complete"
        ;;
        
    update)
        log_info "Updating services..."
        if [ "$DRY_RUN" != "true" ]; then
            docker-compose -f docker-compose-production.yml up -d
            log_info "✅ Update complete"
        else
            log_info "DRY RUN: Would update services"
        fi
        ;;
        
    rollback)
        log_info "Rolling back to previous version..."
        if [ "$DRY_RUN" != "true" ]; then
            # Get previous image version from Git
            PREV_COMMIT=$(git rev-parse HEAD~1)
            log_info "Previous commit: $PREV_COMMIT"
            
            # Rollback would require storing image digests
            log_warn "Rollback not yet implemented. Use manual deployment."
        else
            log_info "DRY RUN: Would rollback to previous version"
        fi
        ;;
        
    stop)
        log_info "Stopping services..."
        if [ "$DRY_RUN" != "true" ]; then
            docker-compose -f docker-compose-production.yml down
            log_info "✅ Services stopped"
        else
            log_info "DRY RUN: Would stop services"
        fi
        ;;
        
    scale)
        REPLICAS="${4:-3}"
        log_info "Scaling to $REPLICAS replicas..."
        if [ "$DRY_RUN" != "true" ]; then
            # For docker-compose, we'd need to use docker swarm or manually scale
            # For K8s: kubectl scale deployment --replicas=$REPLICAS -n engine
            log_info "Scaling through Kubernetes:"
            echo "kubectl scale deployment tenetaiagency-101 --replicas=$REPLICAS -n engine"
            echo "kubectl scale deployment ultimate-engine --replicas=$REPLICAS -n engine"
            echo "kubectl scale deployment engine-365-days --replicas=$REPLICAS -n engine"
            echo "kubectl scale deployment restricted-aichatbot-trader --replicas=$REPLICAS -n engine"
        fi
        ;;
        
    logs)
        log_info "Fetching logs..."
        SERVICE="${4:-}"
        if [ -z "$SERVICE" ]; then
            docker-compose -f docker-compose-production.yml logs -f --tail=100
        else
            docker-compose -f docker-compose-production.yml logs -f --tail=100 $SERVICE
        fi
        ;;
        
    backup)
        log_info "Creating backup..."
        BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
        mkdir -p $BACKUP_DIR
        
        if [ "$DRY_RUN" != "true" ]; then
            # Backup PostgreSQL
            log_info "Backing up PostgreSQL..."
            docker-compose -f docker-compose-production.yml exec -T postgresql \
                pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/postgres.sql.gz
            
            # Backup Redis
            log_info "Backing up Redis..."
            docker-compose -f docker-compose-production.yml exec -T redis \
                redis-cli --rdb $BACKUP_DIR/redis.rdb || true
            
            # Backup configuration
            cp docker-compose-production.yml $BACKUP_DIR/
            cp .env.production $BACKUP_DIR/
            
            log_info "✅ Backup created at $BACKUP_DIR"
        else
            log_info "DRY RUN: Would backup to $BACKUP_DIR"
        fi
        ;;
        
    monitor)
        log_info "Starting monitoring..."
        echo ""
        echo "Dashboard URLs:"
        echo "  Prometheus: http://localhost:9090"
        echo "  Grafana: http://localhost:3000"
        echo "  Jaeger: http://localhost:16686"
        echo "  AlertManager: http://localhost:9093"
        echo ""
        docker-compose -f docker-compose-production.yml logs -f prometheus grafana
        ;;
        
    *)
        log_error "Unknown action: $ACTION"
        echo ""
        echo "Available actions:"
        echo "  deploy      - Deploy all services"
        echo "  update      - Update running services"
        echo "  rollback    - Rollback to previous version"
        echo "  stop        - Stop all services"
        echo "  scale       - Scale services (requires NUM_REPLICAS)"
        echo "  logs        - Stream logs (optional SERVICE)"
        echo "  backup      - Create database backup"
        echo "  monitor     - View monitoring dashboards"
        echo ""
        echo "Usage: $0 <environment> <action> [dry-run] [extra-args]"
        exit 1
        ;;
esac

echo ""
log_info "=========================================="
log_info "Operation completed at $(date)"
