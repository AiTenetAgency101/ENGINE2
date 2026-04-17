# Quick Start - ENGINE System

## 🚀 Start Entire System

```powershell
# Navigate to project directory
cd C:\Users\ENGINE

# Start production stack (Docker Compose)
docker-compose -f docker-compose-production.yml up -d

# OR deploy to Kubernetes
kubectl apply -f k8s/
```

## 📊 Access Dashboards

```powershell
# EHF Performance Dashboard (Human Optimization)
# Open in browser: http://localhost:9001

# Smart Home Dashboard (ZHA Control)
# Open in browser: http://localhost:9000

# Prometheus Metrics
# Open in browser: http://localhost:9090

# Grafana Visualization
# Open in browser: http://localhost:3000

# Jaeger Distributed Tracing
# Open in browser: http://localhost:16686

# AlertManager
# Open in browser: http://localhost:9093
```

## ✅ Verify System Status

```powershell
# Check all services running
docker-compose -f docker-compose-production.yml ps

# Check health
bash scripts/health-check.sh

# View logs
docker-compose -f docker-compose-production.yml logs -f

# Get EHF status
curl http://localhost:9001/api/ehf/status

# Get Smart Home status
curl http://localhost:9000/api/zha/status

# Get TRON status
curl http://localhost:9000/api/tron/status
```

## 🔧 Common Operations

```powershell
# Stop system
docker-compose -f docker-compose-production.yml down

# View specific service logs
docker-compose -f docker-compose-production.yml logs -f [service-name]

# Restart a service
docker-compose -f docker-compose-production.yml restart [service-name]

# Scale services (Kubernetes)
kubectl scale deployment tenetaiagency-101 --replicas=5 -n engine

# View pod logs
kubectl logs -n engine deployment/[service-name] -f
```

## 📈 Monitor Performance

```powershell
# Watch metrics in real-time
# 1. Open http://localhost:9090 (Prometheus)
# 2. Open http://localhost:3000 (Grafana)
# 3. Open http://localhost:9001 (EHF Dashboard)

# Check resource usage
docker-compose -f docker-compose-production.yml stats

# Or Kubernetes
kubectl top pods -n engine
kubectl top nodes
```

## 🧠 Control Smart Home

```powershell
# List all devices
curl http://localhost:9000/api/zha/devices

# Control a device
curl -X POST http://localhost:9000/api/zha/devices/light_living_room/control `
  -H "Content-Type: application/json" `
  -d '{"command": "on"}'

# Activate a scene
curl -X POST http://localhost:9000/api/scenes/morning_routine/activate

# Control device group
curl -X POST http://localhost:9000/api/zha/groups/living_room/control `
  -H "Content-Type: application/json" `
  -d '{"command": "on"}'
```

## 📱 Check Human Performance (EHF)

```powershell
# Get current performance score
curl http://localhost:9001/api/ehf/status

# Get circadian phase
curl http://localhost:9001/api/ehf/circadian

# Get recommendations
curl http://localhost:9001/api/ehf/recommendations

# Update biomarkers
curl -X POST http://localhost:9001/api/ehf/biomarkers `
  -H "Content-Type: application/json" `
  -d '{"heart_rate": 65, "stress": 20, "energy": 85}'
```

## 🎯 Next Steps

1. **Open dashboards in browser** (use links above)
2. **Discover smart devices**: POST /api/zha/devices
3. **Create automation rules**: Use Smart Home dashboard
4. **Monitor performance**: Watch Grafana/EHF dashboards
5. **Adjust settings**: Use REST APIs or web interfaces

---

**Quick Links:**
- Documentation: See `QUICK_REFERENCE.md`
- Deployment: See `PRODUCTION_DEPLOYMENT.md`
- Smart Home: See `ZHA_UNIFIED_GUIDE.md`
- EHF Guide: See `EHF_COMPLETE_GUIDE.md`
