# ENGINE Production System - Quick Reference

## 🚀 One-Command Deployment

```bash
# Docker Compose (Development/Staging)
docker-compose -f docker-compose-production.yml up -d

# Kubernetes (Production)
kubectl apply -f k8s/

# GitHub Actions (Full CI/CD)
git push origin main
```

## 📊 System Overview

| Component | Tech Stack | Port | Purpose |
|-----------|-----------|------|---------|
| **tenetaiagency-101** | Python 3.13 | 8000 | AI Agency Service |
| **ultimate-engine** | Node.js 22 | 3000 | Web API Service |
| **engine-365-days** | Go 1.22 | 8080 | High-Performance Service |
| **restricted-aichatbot-trader** | Python 3.13 | 5000 | Trading Service |
| **PostgreSQL** | Database | 5432 | Persistent Data |
| **Redis** | Cache | 6379 | Session/Cache Store |
| **Vault** | Secrets | 8200 | Secrets Management |
| **Prometheus** | Metrics | 9090 | Metrics Collection |
| **Grafana** | Dashboards | 3000 | Visualization |
| **Jaeger** | Tracing | 16686 | Distributed Tracing |
| **AlertManager** | Alerts | 9093 | Alert Routing |

## 🔑 Critical Configuration

### Secrets (Must Update Before Production)
```bash
# 1. Change database password
DB_PASSWORD=YourStrongPasswordHere!

# 2. Change Redis password
REDIS_PASSWORD=YourStrongPasswordHere!

# 3. Generate Vault token
VAULT_TOKEN=s.yourvaulttokenhere

# 4. Set Slack webhook for alerts
SLACK_WEBHOOK_URL=https://hooks.slack.com/...

# 5. Update .env.production with all values
```

### Environment Variables
- `ENVIRONMENT=production`
- `LOG_LEVEL=INFO`
- `TRACING_ENABLED=true`
- `METRICS_ENABLED=true`

## 📋 Pre-Deployment Checklist

```bash
# 1. Validate configuration
docker-compose config
kubectl apply -f k8s/ --dry-run=client

# 2. Check prerequisites
docker --version
docker-compose --version
kubectl version
git status

# 3. Verify secrets
grep "ChangeMeInProduction" .env.production
# Replace all default values

# 4. Create data directories
mkdir -p data/{postgres,redis,prometheus,grafana,jaeger,vault}

# 5. Test connectivity
ping postgres
redis-cli ping
psql -h localhost -U engine_user -d engine_prod
```

## 🎯 Common Operations

### Health Check
```bash
bash scripts/health-check.sh
```

### View Logs
```bash
# Docker Compose
docker-compose -f docker-compose-production.yml logs -f [service]

# Kubernetes
kubectl logs -n engine deployment/[service] -f
```

### Scale Services
```bash
# Kubernetes HPA (automatic)
kubectl get hpa -n engine -w

# Manual scaling
kubectl scale deployment/[service] --replicas=5 -n engine
```

### Restart Service
```bash
# Docker Compose
docker-compose -f docker-compose-production.yml restart [service]

# Kubernetes
kubectl rollout restart deployment/[service] -n engine
```

### View Metrics
```bash
# Prometheus
open http://localhost:9090

# Grafana
open http://localhost:3000
# Username: admin
# Password: Check .env.production (GRAFANA_PASSWORD)
```

### View Traces
```bash
open http://localhost:16686
```

## 🚨 Troubleshooting Quick Guide

| Issue | Solution |
|-------|----------|
| **Pod crash loops** | `kubectl logs -n engine [pod-name]` |
| **High memory** | `kubectl top pods -n engine` |
| **Connection refused** | Check service health: `curl http://localhost:PORT/health` |
| **Slow queries** | Check PostgreSQL: `kubectl exec -it postgres -- psql -U engine_user` |
| **Cache issues** | `redis-cli INFO` and check memory |
| **Metrics missing** | Verify Prometheus targets: `http://localhost:9090/targets` |

## 📈 Performance Targets

```
Availability:    99.9%
p95 Latency:     <2 seconds
p99 Latency:     <5 seconds
Error Rate:      <0.1%
CPU Usage:       <70% (alert at 85%)
Memory Usage:    <80% (alert at 85%)
Disk Free:       >15% (alert at 15%)
```

## 🔄 Deployment Strategies

### Rolling Update (Default)
- One pod at a time
- Zero downtime
- Safe rollback available

### Blue-Green (Manual)
```bash
# Deploy new version alongside old
kubectl apply -f k8s/v2-deployment.yaml

# Switch traffic
kubectl set service engine selector app=engine-v2

# Keep old for quick rollback
# kubectl set service engine selector app=engine-v1
```

### Canary (Manual)
```bash
# Deploy 10% of traffic to new version
# Monitor metrics
# Gradually increase to 100%
# Keep old version for rollback
```

## 🔐 Security Checklist

- [ ] All default passwords changed
- [ ] Vault initialized and unsealed
- [ ] TLS certificates configured
- [ ] Network policies enabled
- [ ] RBAC roles minimal
- [ ] Secrets not in version control
- [ ] Log aggregation enabled
- [ ] Audit logging configured

## 📞 Support Resources

| Resource | URL/Command |
|----------|------------|
| **Prometheus** | http://localhost:9090 |
| **Grafana** | http://localhost:3000 |
| **Jaeger** | http://localhost:16686 |
| **AlertManager** | http://localhost:9093 |
| **Logs** | `docker-compose logs -f` |
| **Events** | `kubectl get events -n engine` |
| **Deployment Guide** | `PRODUCTION_DEPLOYMENT.md` |

## 🔄 Backup & Recovery

### Automated Backups
```bash
# PostgreSQL daily
docker-compose exec postgresql pg_dump -U engine_user engine_prod | gzip > backup.sql.gz

# Redis
docker-compose exec redis redis-cli BGSAVE

# Kubernetes state
kubectl get all -n engine -o yaml > k8s-state-backup.yaml
```

### Quick Restore
```bash
# PostgreSQL
zcat backup.sql.gz | docker-compose exec -T postgresql psql -U engine_user engine_prod

# Kubernetes
kubectl apply -f k8s-state-backup.yaml
```

## 📊 Monitoring Queries

### Prometheus PromQL Examples
```promql
# Service availability
up{job=~"tenetai|ultimate|engine365|trader"}

# Request rate
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m])

# Latency percentiles
histogram_quantile(0.95, http_request_duration_seconds)

# CPU usage
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# Database connections
pg_stat_activity_count

# Redis memory
redis_memory_used_bytes / redis_memory_max_bytes
```

## 🎯 SLO Monitoring

```
Availability SLO:    99.9% per month
Latency SLO:         95% of requests < 2s
Error Rate SLO:      <0.1% per month

Alert when:
- Availability < 99.9% for 5+ minutes
- p95 latency > 2s for 10+ minutes
- Error rate > 0.1% for 5+ minutes
```

## 📅 Maintenance Windows

```
Backup:              Daily at 2 AM UTC
Database vacuum:     Weekly at 3 AM UTC
Certificate renewal: 30 days before expiry
OS patches:           1st Sunday monthly
Failover test:       Quarterly
Disaster recovery:   Annual
```

## 🚀 Scaling Guide

| Load | Replicas | Action |
|------|----------|--------|
| <100 req/s | 3 | Normal |
| 100-500 req/s | 5-6 | HPA scales up |
| 500-1000 req/s | 8-10 | Add node if needed |
| >1000 req/s | 10+ | Manual scaling required |

## 🔗 Related Documentation

- `PRODUCTION_DEPLOYMENT.md` - Detailed deployment guide
- `.env.production` - Configuration template
- `docker-compose-production.yml` - Full stack definition
- `k8s/deployment.yaml` - Kubernetes manifests
- `.github/workflows/production-deploy.yml` - CI/CD pipeline
- `scripts/` - Automation scripts

## 📞 Getting Help

1. Check health status: `bash scripts/health-check.sh`
2. Review logs: `docker-compose logs [service]`
3. Check Prometheus targets: `http://localhost:9090/targets`
4. Check Grafana dashboards: `http://localhost:3000`
5. Review alert rules: `monitoring/prometheus-rules.yml`
6. Run Kubernetes diagnostics: `kubectl describe pod -n engine [pod-name]`

---

**Status**: ✅ Production Ready
**Version**: 1.0.0
**Last Updated**: $(date)
