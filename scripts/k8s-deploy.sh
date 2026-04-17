#!/bin/bash
# Kubernetes production deployment script

set -euo pipefail

NAMESPACE="engine"
ACTION="${1:-deploy}"
DRY_RUN="${2:-false}"

echo "=========================================="
echo "ENGINE Kubernetes Production Deployment"
echo "=========================================="
echo "Action: $ACTION"
echo "Dry Run: $DRY_RUN"
echo "Timestamp: $(date)"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check kubectl
if ! command -v kubectl &> /dev/null; then
    log_error "kubectl not found. Please install kubectl."
    exit 1
fi

# Validate context
CONTEXT=$(kubectl config current-context)
log_info "Current context: $CONTEXT"

case $ACTION in
    deploy)
        log_info "Deploying to Kubernetes..."
        
        # Create namespace
        log_info "Creating namespace..."
        kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
        
        # Create secrets
        log_info "Creating secrets..."
        kubectl create secret generic engine-db-secret \
            --from-literal=db-user=engine_user \
            --from-literal=db-password=${DB_PASSWORD:-ChangeMeInProduction!} \
            --from-literal=db-name=engine_prod \
            -n $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
        
        kubectl create secret generic engine-redis-secret \
            --from-literal=redis-password=${REDIS_PASSWORD:-ChangeMeInProduction!} \
            -n $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
        
        kubectl create secret generic engine-vault-secret \
            --from-literal=vault-token=${VAULT_TOKEN:-s.changemelater123456789abc} \
            -n $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
        
        # Apply manifests
        if [ "$DRY_RUN" = "true" ]; then
            log_info "DRY RUN: Validating manifests..."
            kubectl apply -f k8s/ --dry-run=client
        else
            log_info "Applying Kubernetes manifests..."
            kubectl apply -f k8s/
            
            # Wait for deployments
            log_info "Waiting for deployments to roll out..."
            deployments=("tenetaiagency-101" "ultimate-engine" "engine-365-days" "restricted-aichatbot-trader")
            
            for deployment in "${deployments[@]}"; do
                log_info "Rolling out $deployment..."
                kubectl rollout status deployment/$deployment -n $NAMESPACE --timeout=5m
            done
        fi
        
        log_info "✅ Deployment complete"
        ;;
        
    verify)
        log_info "Verifying deployment..."
        
        log_info "Pods:"
        kubectl get pods -n $NAMESPACE -o wide
        
        log_info ""
        log_info "Services:"
        kubectl get services -n $NAMESPACE
        
        log_info ""
        log_info "HPAs:"
        kubectl get hpa -n $NAMESPACE
        
        log_info ""
        log_info "Pod status:"
        kubectl get pods -n $NAMESPACE -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.conditions[?(@.type=="Ready")].status}{"\n"}{end}'
        ;;
        
    logs)
        DEPLOYMENT="${3:-}"
        if [ -z "$DEPLOYMENT" ]; then
            log_error "Specify deployment name"
            echo "Usage: $0 logs <deployment-name>"
            exit 1
        fi
        
        log_info "Tailing logs for $DEPLOYMENT..."
        kubectl logs -n $NAMESPACE deployment/$DEPLOYMENT -f --timestamps=true --all-containers=true
        ;;
        
    scale)
        DEPLOYMENT="${3:-}"
        REPLICAS="${4:-3}"
        
        if [ -z "$DEPLOYMENT" ]; then
            log_error "Specify deployment name and replica count"
            exit 1
        fi
        
        log_info "Scaling $DEPLOYMENT to $REPLICAS replicas..."
        if [ "$DRY_RUN" != "true" ]; then
            kubectl scale deployment/$DEPLOYMENT --replicas=$REPLICAS -n $NAMESPACE
            kubectl rollout status deployment/$DEPLOYMENT -n $NAMESPACE --timeout=5m
            log_info "✅ Scaling complete"
        else
            log_info "DRY RUN: Would scale $DEPLOYMENT to $REPLICAS replicas"
        fi
        ;;
        
    restart)
        DEPLOYMENT="${3:-}"
        
        if [ -z "$DEPLOYMENT" ]; then
            log_error "Specify deployment name"
            exit 1
        fi
        
        log_info "Restarting $DEPLOYMENT..."
        if [ "$DRY_RUN" != "true" ]; then
            kubectl rollout restart deployment/$DEPLOYMENT -n $NAMESPACE
            kubectl rollout status deployment/$DEPLOYMENT -n $NAMESPACE --timeout=5m
            log_info "✅ Restart complete"
        else
            log_info "DRY RUN: Would restart $DEPLOYMENT"
        fi
        ;;
        
    upgrade)
        IMAGE="${3:-}"
        TAG="${4:-latest}"
        
        if [ -z "$IMAGE" ]; then
            log_error "Specify image name"
            exit 1
        fi
        
        log_info "Upgrading deployment with new image..."
        DEPLOYMENT=$(echo $IMAGE | sed 's/.*\///' | sed 's/:.*//g')
        
        if [ "$DRY_RUN" != "true" ]; then
            kubectl set image deployment/$DEPLOYMENT \
                $DEPLOYMENT=$IMAGE:$TAG \
                -n $NAMESPACE
            
            kubectl rollout status deployment/$DEPLOYMENT -n $NAMESPACE --timeout=5m
            log_info "✅ Upgrade complete"
        else
            log_info "DRY RUN: Would upgrade $DEPLOYMENT to $IMAGE:$TAG"
        fi
        ;;
        
    rollback)
        DEPLOYMENT="${3:-}"
        
        if [ -z "$DEPLOYMENT" ]; then
            log_error "Specify deployment name"
            exit 1
        fi
        
        log_info "Rolling back $DEPLOYMENT to previous version..."
        if [ "$DRY_RUN" != "true" ]; then
            kubectl rollout undo deployment/$DEPLOYMENT -n $NAMESPACE
            kubectl rollout status deployment/$DEPLOYMENT -n $NAMESPACE --timeout=5m
            log_info "✅ Rollback complete"
        else
            log_info "DRY RUN: Would rollback $DEPLOYMENT"
        fi
        ;;
        
    status)
        log_info "Deployment status:"
        
        log_info "Replicas:"
        kubectl get deployment -n $NAMESPACE -o wide
        
        log_info ""
        log_info "Pod resource usage:"
        kubectl top pods -n $NAMESPACE
        
        log_info ""
        log_info "HPA status:"
        kubectl get hpa -n $NAMESPACE -o wide
        
        log_info ""
        log_info "Events:"
        kubectl get events -n $NAMESPACE --sort-by='.lastTimestamp' | tail -20
        ;;
        
    backup)
        log_info "Creating Kubernetes backup..."
        BACKUP_DIR="backups/k8s-$(date +%Y%m%d_%H%M%S)"
        mkdir -p $BACKUP_DIR
        
        if [ "$DRY_RUN" != "true" ]; then
            log_info "Exporting all resources..."
            kubectl get all -n $NAMESPACE -o yaml > $BACKUP_DIR/all-resources.yaml
            
            log_info "Exporting secrets..."
            kubectl get secrets -n $NAMESPACE -o yaml > $BACKUP_DIR/secrets.yaml
            
            log_info "Exporting configmaps..."
            kubectl get configmaps -n $NAMESPACE -o yaml > $BACKUP_DIR/configmaps.yaml
            
            log_info "Exporting PVCs..."
            kubectl get pvc -n $NAMESPACE -o yaml > $BACKUP_DIR/pvcs.yaml
            
            log_info "✅ Backup created at $BACKUP_DIR"
        else
            log_info "DRY RUN: Would backup to $BACKUP_DIR"
        fi
        ;;
        
    monitor)
        log_info "Port forwarding for monitoring..."
        
        log_info "Starting port forwards (Ctrl+C to stop)..."
        log_info "  Prometheus: http://localhost:9090"
        log_info "  Grafana: http://localhost:3000"
        log_info "  Jaeger: http://localhost:16686"
        
        # This would typically run in background
        # kubectl port-forward -n $NAMESPACE svc/prometheus 9090:9090 &
        # kubectl port-forward -n $NAMESPACE svc/grafana 3000:3000 &
        # kubectl port-forward -n $NAMESPACE svc/jaeger 16686:16686 &
        
        kubectl port-forward -n $NAMESPACE service/prometheus 9090:9090
        ;;
        
    delete)
        log_warn "This will delete all ENGINE resources from Kubernetes!"
        read -p "Are you sure? (yes/no): " confirm
        
        if [ "$confirm" = "yes" ]; then
            log_info "Deleting namespace $NAMESPACE..."
            if [ "$DRY_RUN" != "true" ]; then
                kubectl delete namespace $NAMESPACE
                log_info "✅ Namespace deleted"
            else
                log_info "DRY RUN: Would delete namespace $NAMESPACE"
            fi
        else
            log_info "Cancelled"
        fi
        ;;
        
    *)
        log_error "Unknown action: $ACTION"
        echo ""
        echo "Available actions:"
        echo "  deploy          - Deploy to Kubernetes"
        echo "  verify          - Verify deployment status"
        echo "  logs <deploy>   - View logs for deployment"
        echo "  scale <deploy> <num>  - Scale deployment"
        echo "  restart <deploy>      - Restart deployment"
        echo "  upgrade <image> <tag> - Upgrade with new image"
        echo "  rollback <deploy>     - Rollback to previous version"
        echo "  status          - Show deployment status"
        echo "  backup          - Backup Kubernetes resources"
        echo "  monitor         - Port forward monitoring services"
        echo "  delete          - Delete all ENGINE resources"
        echo ""
        echo "Usage: $0 <action> [dry-run] [extra-args]"
        exit 1
        ;;
esac

echo ""
log_info "=========================================="
log_info "Operation completed at $(date)"
