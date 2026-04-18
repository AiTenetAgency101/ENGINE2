param(
    [int]$MaxLogDays = 7,
    [int]$MaxLogTotalMB = 500
)

$root    = "C:\ENGINE2"
$logsDir = Join-Path $root "LOGS"
$stateDir = Join-Path $root "STATE"
$summaryDir = Join-Path $root "SUMMARY"

New-Item -ItemType Directory -Path $logsDir,$stateDir,$summaryDir -Force | Out-Null

# --- STORM: write a small present-moment state snapshot ---
$state = [pscustomobject]@{
    timestamp_utc = (Get-Date).ToUniversalTime().ToString("o")
    host          = $env:COMPUTERNAME
    user          = $env:USERNAME
    free_gb_c     = [math]::Round((Get-PSDrive C).Free/1GB,2)
}
$statePath = Join-Path $stateDir "state.json"
$state | ConvertTo-Json -Depth 5 | Set-Content -Path $statePath -Encoding UTF8

# --- COOL: rotate logs by day, cap age and total size ---
$todayLogDir = Join-Path $logsDir (Get-Date -Format "yyyy-MM-dd")
New-Item -ItemType Directory -Path $todayLogDir -Force | Out-Null

$logFile = Join-Path $todayLogDir "events.log"
"[{0}] heartbeat free_gb_c={1}" -f (Get-Date -Format "o"), $state.free_gb_c | Add-Content -Path $logFile -Encoding UTF8

# delete logs older than MaxLogDays
Get-ChildItem $logsDir -Directory |
    Where-Object {
        $_.Name -match '^\d{4}-\d{2}-\d{2}$' -and
        ([datetime]$_.Name) -lt (Get-Date).Date.AddDays(-$MaxLogDays)
    } |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# cap total log size
$allLogs = Get-ChildItem $logsDir -Recurse -File -ErrorAction SilentlyContinue
$totalBytes = ($allLogs | Measure-Object Length -Sum).Sum
$maxBytes = $MaxLogTotalMB * 1MB

if ($totalBytes -gt $maxBytes) {
    $toDelete = $allLogs | Sort-Object LastWriteTime | Where-Object { $totalBytes -gt $maxBytes }
    foreach ($f in $toDelete) {
        $totalBytes -= $f.Length
        Remove-Item $f.FullName -Force -ErrorAction SilentlyContinue
        if ($totalBytes -le $maxBytes) { break }
    }
}

# --- RETURN: write a tiny daily summary ---
$summaryFile = Join-Path $summaryDir ((Get-Date -Format "yyyy-MM-dd") + ".json")
$summary = [pscustomobject]@{
    date        = (Get-Date -Format "yyyy-MM-dd")
    last_utc    = $state.timestamp_utc
    free_gb_c   = $state.free_gb_c
    log_dirs    = (Get-ChildItem $logsDir -Directory | Select-Object -ExpandProperty Name)
}
$summary | ConvertTo-Json -Depth 5 | Set-Content -Path $summaryFile -Encoding UTF8
