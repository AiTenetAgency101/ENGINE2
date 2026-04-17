#!/usr/bin/env bash
set -e

echo "=== ENGINE2 K8S DEPLOY ORCHESTRATOR ==="

echo "Applying manifests..."
kubectl apply -f k8s/

echo "Waiting for pods..."
kubectl get pods -A

echo "Checking logs..."
kubectl logs -l app=engine2 --tail=50 || true

echo "=== DEPLOYMENT COMPLETE ==="
