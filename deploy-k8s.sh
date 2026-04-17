#!/bin/bash
# Deploy full stack to Kubernetes

set -e

echo "🚀 Deploying ENGINE v1.0.0 to Kubernetes..."

# Create namespace
kubectl create namespace engine-system --dry-run=client -o yaml | kubectl apply -f -

# Apply storage
echo "📦 Applying ATA storage configuration..."
kubectl apply -f k8s-ata-storage.yaml

# Wait for storage
sleep 5

# Apply deployments
echo "🔄 Deploying engines..."
kubectl apply -f k8s-engines-deployment.yaml

# Wait for deployments
echo "⏳ Waiting for deployments to be ready..."
kubectl rollout status deployment/engine-365-days --timeout=300s
kubectl rollout status deployment/ultimate-engine --timeout=300s
kubectl rollout status deployment/tenetaiagency-101 --timeout=300s

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Engine Status:"
kubectl get pods -l app=engine
echo ""
echo "Services:"
kubectl get svc engine-service
echo ""
echo "Storage:"
kubectl get pvc
