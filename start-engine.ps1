# ENGINE System - Quick Start Script for PowerShell
# Usage: .\start-engine.ps1

Write-Host "==========================================" -ForegroundColor Green
Write-Host "ENGINE SYSTEM - QUICK START" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# Check if Docker is running
Write-Host "[1/5] Checking Docker Desktop..." -ForegroundColor Cyan
$dockerRunning = $false
try {
    $dockerStatus = docker ps 2>$null
    if ($dockerStatus) {
        Write-Host "OK Docker is running" -ForegroundColor Green
        $dockerRunning = $true
    }
}
catch {
    Write-Host "NOT OK Docker Desktop is not running" -ForegroundColor Red
}

if (-not $dockerRunning) {
    Write-Host "Please start Docker Desktop first" -ForegroundColor Red
    exit 1
}

# Check if docker-compose-production.yml exists
Write-Host "[2/5] Checking configuration..." -ForegroundColor Cyan
if (Test-Path "docker-compose-production.yml") {
    Write-Host "OK docker-compose-production.yml found" -ForegroundColor Green
} else {
    Write-Host "NOT OK docker-compose-production.yml not found" -ForegroundColor Red
    exit 1
}

# Start services
Write-Host "[3/5] Starting ENGINE services..." -ForegroundColor Cyan
docker-compose -f docker-compose-production.yml up -d
if ($LASTEXITCODE -eq 0) {
    Write-Host "OK Services started" -ForegroundColor Green
} else {
    Write-Host "NOT OK Failed to start services" -ForegroundColor Red
    exit 1
}

# Wait for services to be ready
Write-Host "[4/5] Waiting for services to initialize..." -ForegroundColor Cyan
Start-Sleep -Seconds 30

# Check health
Write-Host "[5/5] Checking service health..." -ForegroundColor Cyan
$healthCheck = docker-compose -f docker-compose-production.yml ps 2>$null
if ($healthCheck -match "Up") {
    Write-Host "OK Services are starting up" -ForegroundColor Green
} else {
    Write-Host "NOTICE Services initializing (may take 30 more seconds)" -ForegroundColor Yellow
}

# Print dashboard links
Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "DASHBOARDS READY - OPEN IN BROWSER:" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "1. EHF Performance Dashboard" -ForegroundColor Yellow
Write-Host "   http://localhost:9001" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Smart Home Control Dashboard" -ForegroundColor Yellow
Write-Host "   http://localhost:9000" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Prometheus Metrics" -ForegroundColor Yellow
Write-Host "   http://localhost:9090" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Grafana Visualization" -ForegroundColor Yellow
Write-Host "   http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "5. Jaeger Distributed Tracing" -ForegroundColor Yellow
Write-Host "   http://localhost:16686" -ForegroundColor Cyan
Write-Host ""
Write-Host "6. AlertManager" -ForegroundColor Yellow
Write-Host "   http://localhost:9093" -ForegroundColor Cyan
Write-Host ""

# Print status command
Write-Host "==========================================" -ForegroundColor Green
Write-Host "USEFUL COMMANDS:" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Check service status:" -ForegroundColor Yellow
Write-Host "   docker-compose -f docker-compose-production.yml ps" -ForegroundColor Cyan
Write-Host ""
Write-Host "View logs:" -ForegroundColor Yellow
Write-Host "   docker-compose -f docker-compose-production.yml logs -f" -ForegroundColor Cyan
Write-Host ""
Write-Host "Stop services:" -ForegroundColor Yellow
Write-Host "   docker-compose -f docker-compose-production.yml down" -ForegroundColor Cyan
Write-Host ""
Write-Host "Check health:" -ForegroundColor Yellow
Write-Host "   bash scripts/health-check.sh" -ForegroundColor Cyan
Write-Host ""

Write-Host "==========================================" -ForegroundColor Green
Write-Host "SUCCESS ENGINE SYSTEM STARTED" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
