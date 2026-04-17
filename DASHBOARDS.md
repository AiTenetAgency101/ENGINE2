# 🎯 ENGINE DASHBOARDS - Quick Access Guide

## ✅ All Dashboards Available

After running `docker-compose up -d`, open these URLs in your browser:

### 1️⃣ EHF Performance Dashboard (Port 9001)
```
http://localhost:9001
```
**What you'll see:**
- Real-time performance score (0-100%)
- Circadian phase (morning, afternoon, evening, etc.)
- Cognitive state (peak focus, deep work, recovery, etc.)
- Biomarkers: Heart rate, stress, energy, sleep quality
- Personalized recommendations
- EHF-TRON alignment status

**Perfect for:** Personal performance optimization, health tracking, cognitive state monitoring

---

### 2️⃣ Smart Home Control Dashboard (Port 9000)
```
http://localhost:9000
```
**What you'll see:**
- All smart devices (Zigbee + Chinese IoT)
- Device status and control
- Smart scenes (morning, evening, away, sleep)
- Automation rules
- Device groups
- Real-time state changes

**Perfect for:** Smart home control, device management, automation setup

---

### 3️⃣ Prometheus Metrics (Port 9090)
```
http://localhost:9090
```
**What you'll see:**
- System metrics: CPU, memory, disk, network
- Application metrics: Request rate, latency, errors
- Container metrics
- Health status of all services

**Perfect for:** Performance monitoring, metric queries, troubleshooting

---

### 4️⃣ Grafana Dashboards (Port 3000)
```
http://localhost:3000
```
**Default Login:**
- Username: `admin`
- Password: `admin` (change on first login)

**What you'll see:**
- System dashboard (CPU, memory, disk)
- Application dashboard (requests, latency, errors)
- Container metrics
- Network traffic
- Database performance

**Perfect for:** Visualization, alerting, long-term trends

---

### 5️⃣ Jaeger Distributed Tracing (Port 16686)
```
http://localhost:16686
```
**What you'll see:**
- Distributed traces across all services
- Request flow visualization
- Latency breakdown by component
- Error traces
- Service dependencies

**Perfect for:** Performance analysis, debugging, understanding request flow

---

### 6️⃣ AlertManager (Port 9093)
```
http://localhost:9093
```
**What you'll see:**
- Active alerts
- Alert history
- Alert routing configuration
- Integration status (Slack, PagerDuty)

**Perfect for:** Alert management, incident response

---

## 🚀 Quick Start Commands

### Start Everything
```powershell
# Navigate to project directory
cd C:\Users\ENGINE

# Start all services
docker-compose -f docker-compose-production.yml up -d
```

### Check All Services Are Running
```powershell
# See running containers
docker-compose -f docker-compose-production.yml ps
```

### View Logs
```powershell
# View all logs (live)
docker-compose -f docker-compose-production.yml logs -f

# View specific service logs
docker-compose -f docker-compose-production.yml logs -f prometheus
docker-compose -f docker-compose-production.yml logs -f grafana
docker-compose -f docker-compose-production.yml logs -f zha-tron-engine
```

### Stop Services
```powershell
# Stop all services
docker-compose -f docker-compose-production.yml down

# Stop and remove volumes
docker-compose -f docker-compose-production.yml down -v
```

---

## 📊 What Each Dashboard Shows

| Dashboard | Port | Purpose | Best For |
|-----------|------|---------|----------|
| **EHF** | 9001 | Human performance | Personal health & optimization |
| **Smart Home** | 9000 | Device control | Home automation |
| **Prometheus** | 9090 | Metrics collection | System monitoring |
| **Grafana** | 3000 | Visualization | Dashboards & alerting |
| **Jaeger** | 16686 | Distributed tracing | Performance debugging |
| **AlertManager** | 9093 | Alert management | Incident response |

---

## 🔗 API Endpoints (if you prefer CLI)

### EHF API
```powershell
# Get performance status
curl http://localhost:9001/api/ehf/status

# Get recommendations
curl http://localhost:9001/api/ehf/recommendations

# Get circadian phase
curl http://localhost:9001/api/ehf/circadian
```

### Smart Home API
```powershell
# List all devices
curl http://localhost:9000/api/zha/devices

# Get smart home status
curl http://localhost:9000/api/zha/status

# Activate a scene
curl -X POST http://localhost:9000/api/scenes/morning_routine/activate
```

### TRON API
```powershell
# Get TRON grid status
curl http://localhost:9000/api/tron/status
```

---

## ✨ Default Credentials

| Service | Username | Password | Notes |
|---------|----------|----------|-------|
| Grafana | admin | admin | ⚠️ Change on first login |
| AlertManager | N/A | N/A | No authentication |
| Prometheus | N/A | N/A | No authentication |
| EHF API | N/A | N/A | No authentication (local) |

---

## 🆘 Troubleshooting

### Dashboards Not Loading?
```powershell
# 1. Check if services are running
docker-compose -f docker-compose-production.yml ps

# 2. Check logs
docker-compose -f docker-compose-production.yml logs -f

# 3. Wait 30 seconds (services take time to start)
# 4. Try again
```

### Port Already in Use?
```powershell
# Find what's using port 9001
netstat -ano | findstr :9001

# Or change ports in docker-compose-production.yml
# ports: "9002:9001"  # Map external port 9002 to container port 9001
```

### Can't Connect to Docker?
```powershell
# Restart Docker Desktop:
# 1. Close Docker Desktop
# 2. Wait 10 seconds
# 3. Reopen Docker Desktop
# 4. Wait for "Docker Desktop is running"
# 5. Try again
```

---

## 📚 Documentation Links

- **Production Deployment**: See `PRODUCTION_DEPLOYMENT.md`
- **Quick Reference**: See `QUICK_REFERENCE.md`
- **Smart Home Guide**: See `ZHA_UNIFIED_GUIDE.md`
- **EHF Guide**: See `EHF_COMPLETE_GUIDE.md`
- **System Overview**: See `COMPLETE_SYSTEM_SUMMARY.md`

---

## 🎉 You're All Set!

All dashboards are now accessible. Start with:

1. **EHF Dashboard** (http://localhost:9001) - Check your performance
2. **Smart Home** (http://localhost:9000) - Control your devices
3. **Grafana** (http://localhost:3000) - Monitor system health

Enjoy! 🚀
