# ENGINE SYSTEM - START HERE

## ⚠️ IMPORTANT: Dashboard Access Instructions

The lines below are **NOT PowerShell commands**. They are just showing you where to open in your browser.

### After starting the system with `.\start-engine.ps1`, open these URLs:

**Copy and paste each link into your web browser address bar:**

```
# Copy this URL into your browser:
http://localhost:9001
```
👆 This is your EHF Performance Dashboard

```
# Copy this URL into your browser:
http://localhost:9000
```
👆 This is your Smart Home Dashboard

```
# Copy this URL into your browser:
http://localhost:9090
```
👆 This is Prometheus (Metrics)

```
# Copy this URL into your browser:
http://localhost:3000
```
👆 This is Grafana (Visualization)

```
# Copy this URL into your browser:
http://localhost:16686
```
👆 This is Jaeger (Distributed Tracing)

```
# Copy this URL into your browser:
http://localhost:9093
```
👆 This is AlertManager

---

## 🚀 Starting the System (CORRECT WAY)

### Step 1: Open PowerShell

Press `Win + X` then select "Windows PowerShell (Admin)"

### Step 2: Navigate to project directory

```powershell
cd C:\Users\ENGINE
```

### Step 3: Run the startup script

```powershell
.\start-engine.ps1
```

### Step 4: Wait for completion message

You should see:
```
✓ ENGINE SYSTEM STARTED SUCCESSFULLY
```

### Step 5: Open dashboards in browser

Copy one of the URLs above into your browser address bar. For example:

Open your browser and type (or copy/paste):
```
http://localhost:9001
```

Then press Enter.

---

## ⚠️ If you see PowerShell errors like:

```
EHF: : The term 'EHF:' is not recognized
```

**This means:** You tried to run a dashboard URL as a PowerShell command.

**The fix:** Paste the URL into your **web browser**, not PowerShell.

---

## ✅ What You Should See

### After `.\start-engine.ps1` runs:

```
===========================================
ENGINE SYSTEM - QUICK START
===========================================

[1/5] Checking Docker Desktop...
✓ Docker is running

[2/5] Checking configuration...
✓ docker-compose-production.yml found

[3/5] Starting ENGINE services...
✓ Services started

[4/5] Waiting for services to initialize...

[5/5] Checking service health...
✓ Services are starting up

===========================================
DASHBOARDS READY - OPEN IN BROWSER:
===========================================

1. EHF Performance Dashboard
   http://localhost:9001

2. Smart Home Control Dashboard
   http://localhost:9000

3. Prometheus Metrics
   http://localhost:9090

4. Grafana Visualization
   http://localhost:3000

5. Jaeger Distributed Tracing
   http://localhost:16686

6. AlertManager
   http://localhost:9093

===========================================
✓ ENGINE SYSTEM STARTED SUCCESSFULLY
===========================================
```

---

## 📋 Quick Command Reference

### In PowerShell (correct usage):

```powershell
# Check if services are running
docker-compose -f docker-compose-production.yml ps

# View logs
docker-compose -f docker-compose-production.yml logs -f

# Run health check
bash scripts/health-check.sh

# Stop all services
docker-compose -f docker-compose-production.yml down
```

### In Browser (where to open dashboards):

```
http://localhost:9001     # EHF Dashboard
http://localhost:9000     # Smart Home
http://localhost:9090     # Prometheus
http://localhost:3000     # Grafana
http://localhost:16686    # Jaeger
http://localhost:9093     # AlertManager
```

---

## 🎯 Typical First-Time Flow

1. **Open PowerShell** in `C:\Users\ENGINE`
2. **Run**: `.\start-engine.ps1`
3. **Wait**: 30 seconds
4. **Open Browser**: http://localhost:9001
5. **Done!** You're in the EHF Performance dashboard

---

## 🆘 Troubleshooting

### "Docker Desktop is not running"
**Fix:** Open Docker Desktop application and wait for it to fully load

### "docker-compose-production.yml not found"
**Fix:** Make sure you're in `C:\Users\ENGINE` directory
```powershell
pwd   # Check current directory
cd C:\Users\ENGINE   # If not there, change to this
```

### Dashboard won't load
**Fix:** Wait another 30 seconds. Services take time to initialize.
Then try refreshing the page (F5)

### PowerShell error about script not recognized
**Fix:** Allow script execution
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try again: `.\start-engine.ps1`

---

## ✅ Success Indicators

You'll know it's working when:
- [ ] `.\start-engine.ps1` completes without errors
- [ ] http://localhost:9001 loads in browser
- [ ] http://localhost:9000 loads in browser
- [ ] You can see the dashboard content
- [ ] Docker Desktop shows 15 containers running

---

**START HERE:**
1. `.\start-engine.ps1`
2. Wait 30 seconds
3. Open http://localhost:9001 in browser

That's it! 🎉
