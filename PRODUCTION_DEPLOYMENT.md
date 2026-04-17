# ENGINE Production Deployment Guide

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   PRODUCTION STACK                      │
├─────────────────────────────────────────────────────────┤
│  Load Balancer / Ingress                                │
├─────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────┐ │
│  │            APPLICATION SERVICES                    │ │
│  │  ┌──────────┬──────────┬──────────┬─────────────┐  │ │
│  │  │ tenetai  │ ultimate │ engine   │ trader      │  │ │
│  │  │ (Py)     │ (Node)   │ (Go)     │ (Py)        │  │ │
│  │  │ 8000     │ 3000     │ 8080     │ 5000        │  │ │
│  │  └────┬─────┴────┬─────┴────┬────┴────┬────────┘  │ │
│  └───────┼──────────┼──────────┼─────────┼──────────┘ │
│          │          │          │         │             │
│  ┌───────v──────────v──────────v─────────v──────────┐ │
│  │        INFRASTRUCTURE LAYER                       │ │
│  │  ┌────────────┬────────────┬────────────────────┐ │ │
│  │  │ PostgreSQL │   Redis    │   Vault Secrets    │ │ │
│  │  │ 5432       │   6379     │   8200             │ │ │
│  │  └────────────┴────────────┴────────────────────┘ │ │
│  └────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────┐ │
│  │        OBSERVABILITY STACK                         │ │
│  │  Prometheus (9090) → Grafana (3000) → AlertMgr    │ │
│  │  Jaeger (16686) → Distributed Tracing             │ │
│  │  Node-Exporter → Host Metrics                      │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Option 1: Docker Compose (Immediate Deployment)

```bash
# 1. Navigate to project
cd C:\Users\ENGINE

# 2. Create data directories
mkdir -p data/{postgres,redis,prometheus,grafana,jaeger,vault}

# 3. Update .env.production with real secrets
cp .env.production .env.local
# Edit .env.local with actual production values

# 4. Deploy entire stack
docker-compose -f docker-compose-production.yml up -d

# 5. Verify all services
docker-compose -f docker-compose-production.yml ps

# 6. Check health
curl http://localhost:8000/health
curl http://localhost:3000/health
curl http://localhost:8080/health
curl http://localhost:5000/health

# 7. Access dashboards
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/ChangeMeInProduction!)
# Jaeger: http://localhost:16686
# AlertManager: http://localhost:9093
```

### Option 2: Kubernetes (Scalable Production)

```bash
# 1. Create namespace & secrets
kubectl apply -f k8s/

# 2. Verify deployment
kubectl get pods -n engine
kubectl get services -n engine
kubectl get hpa -n engine

# 3. Monitor rollout
kubectl rollout status deployment/tenetaiagency-101 -n engine

# 4. Access services
kubectl port-forward -n engine svc/tenetaiagency-101 8000:8000
kubectl port-forward -n engine svc/ultimate-engine 3000:3000

# 5. Watch auto-scaling
kubectl get hpa -n engine -w
```

### Option 3: GitHub Actions (Automated CI/CD)

```bash
# 1. Push to main branch
git push origin main

# 2. GitHub Actions will:
#    - Run security scans (Trivy)
#    - Lint & test code
#    - Build Docker images
#    - Deploy to K8s
#    - Run health checks
#    - Send Slack notifications

# 3. Monitor workflow
# https://github.com/YOUR_REPO/actions
```

## 🔒 Security Hardening

### 1. Secrets Management
```bash
# Using Vault
export VAULT_ADDR="http://vault:8200"
export VAULT_TOKEN="s.changemelater123456789abc"

# Store secrets
vault kv put secret/engine/db password=ChangeMeInProduction!
vault kv put secret/engine/redis password=ChangeMeInProduction!

# Retrieve in containers via sidecars
```

### 2. Network Security
- NetworkPolicy restricts pod-to-pod communication
- Only allows traffic on app ports (8000, 3000, 8080, 5000)
- Database access restricted to app pods only
- Egress limited to necessary services

### 3. Container Security
- Non-root users (UID 1000)
- Read-only root filesystems
- Dropped capabilities (CAP_ALL)
- SecurityContext enforces:
  - No privilege escalation
  - No new privileges
  - Read-only filesystem

### 4. Pod Security
- PodSecurityPolicy (or Pod Security Standards in K8s 1.25+)
- Network policies for service-to-service communication
- RBAC with minimal required permissions

## 📈 Monitoring & Observability

### Prometheus Metrics
```bash
# Query metrics
curl http://localhost:9090/api/v1/query?query=up

# Common queries
up{job=~"tenetai|ultimate|engine365|trader"}
rate(http_requests_total[5m])
histogram_quantile(0.95, http_request_duration_seconds)
```

### Grafana Dashboards
- **System**: Node exporter metrics, CPU/Memory/Disk
- **Applications**: Request rate, latency, error rate
- **Database**: Connections, queries, replication
- **Cache**: Memory usage, evictions, hit rate
- **Services**: Deployment status, replica count, HPA activity

### Alert Rules
Configured in `monitoring/prometheus-rules.yml`:
- Container availability
- High resource usage
- Database connection limits
- Cache evictions
- SLO violations (99.9% availability, <2s p95 latency)

### Jaeger Distributed Tracing
```bash
# Access UI
open http://localhost:16686

# View traces across services
# Monitor latency distribution
# Identify bottlenecks
```

## 🔄 Zero-Downtime Deployments

### Rolling Update Strategy
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```

This ensures:
1. One new pod starts
2. Health checks pass
3. Old pod terminates
4. Process repeats for all replicas

### Health Checks
```yaml
livenessProbe:
  httpGet: /health
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet: /ready
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 3
```

## 🎯 Auto-Scaling Configuration

### Horizontal Pod Autoscaler (HPA)
```yaml
minReplicas: 3
maxReplicas: 10

metrics:
  - CPU: 70% utilization
  - Memory: 80% utilization

scaleUp: Aggressive (double or +2 pods every 30s)
scaleDown: Conservative (50% reduction every 60s)
```

### Expected Scaling Behavior
```
Under normal load:     3 replicas
Rising to 500 req/s:   6 replicas (2 min)
Peak at 1000 req/s:    10 replicas (2 min)
Returning to normal:   3 replicas (5 min)
```

## 📊 Performance Targets

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Availability | 99.9% | <99.9% |
| p95 Latency | <2s | >2s |
| p99 Latency | <5s | >5s |
| Error Rate | <0.1% | >0.1% |
| CPU Usage | <70% | >85% |
| Memory Usage | <80% | >85% |
| Disk Free | >15% | <15% |

## 🔧 Troubleshooting

### Pod Crashes
```bash
# Check logs
kubectl logs -n engine <pod-name>

# Check events
kubectl describe pod -n engine <pod-name>

# Check resource limits
kubectl top pod -n engine

# Check readiness probe
kubectl get pod -n engine <pod-name> -o jsonpath='{.status.conditions}'
```

### Database Connection Issues
```bash
# Check postgres pod
kubectl logs -n engine engine-postgres-*

# Test connection
kubectl run -it --image=postgres:16-alpine --rm db-test -- \
  psql -h postgres -U engine_user -d engine_prod -c "SELECT 1"
```

### Slow Queries
```bash
# Enable postgres query logging
kubectl set env deployment/postgres \
  -n engine \
  POSTGRES_INITDB_ARGS="-c log_min_duration_statement=1000"

# Check slow query log
kubectl logs -n engine engine-postgres-* | grep "duration:"
```

### Cache Issues
```bash
# Check redis
kubectl logs -n engine engine-redis-*

# Redis info
kubectl exec -n engine engine-redis-* -- redis-cli INFO
```

## 🚨 Incident Response

### Service Down
1. Check service status: `kubectl get pods -n engine`
2. Check recent events: `kubectl get events -n engine --sort-by='.lastTimestamp'`
3. Check logs: `kubectl logs -n engine <pod-name> --tail=100`
4. Restart pod if needed: `kubectl rollout restart deployment/<service> -n engine`

### High Latency
1. Check CPU/Memory: `kubectl top pods -n engine`
2. Check database: `psql -c "SELECT count(*) FROM pg_stat_activity"`
3. Check redis: `redis-cli INFO`
4. Check network: `kubectl get networkpolicy -n engine`

### Database Issues
1. Check connections: `SELECT count(*) FROM pg_stat_activity`
2. Cancel long queries: `SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state='active' AND query_start < now() - interval '10 minutes'`
3. Check disk: `df -h /var/lib/postgresql/data`

## 🔄 Backup & Disaster Recovery

### Automated Backups
```bash
# PostgreSQL daily backup
kubectl exec -n engine engine-postgres-* -- \
  pg_dump -U engine_user engine_prod | gzip > backup.sql.gz

# Redis snapshot
kubectl exec -n engine engine-redis-* -- redis-cli BGSAVE

# Kubernetes state (etcd backup)
kubectl get all -n engine -o yaml > k8s-state-backup.yaml
```

### Restore Procedures
```bash
# Restore PostgreSQL
zcat backup.sql.gz | \
  kubectl exec -i engine-postgres-* -- \
  psql -U engine_user engine_prod

# Restore K8s state
kubectl apply -f k8s-state-backup.yaml
```

## 📋 Pre-Deployment Checklist

- [ ] All environment variables in `.env.production` updated
- [ ] Database credentials changed from defaults
- [ ] Vault token generated and stored securely
- [ ] Redis password set
- [ ] TLS certificates configured
- [ ] Slack/PagerDuty webhooks configured
- [ ] RBAC roles reviewed
- [ ] NetworkPolicies tested
- [ ] PersistentVolume storage allocated
- [ ] Monitoring dashboards created
- [ ] Alert thresholds reviewed
- [ ] Disaster recovery plan tested
- [ ] Load testing completed
- [ ] Documentation reviewed

## 📞 Support & Documentation

- **Logs**: `docker-compose logs -f [service]` or `kubectl logs -n engine [pod]`
- **Metrics**: http://localhost:9090 (Prometheus)
- **Dashboards**: http://localhost:3000 (Grafana)
- **Traces**: http://localhost:16686 (Jaeger)
- **API Docs**: See individual service README files

---

**Status**: ✅ Production Ready
**Last Updated**: $(date)
**Deployment Version**: 1.0.0
