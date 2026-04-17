# MCP Configuration Guide for ENGINE v1.0.0

## Overview
This guide explains how to configure and use MCP (Model Context Protocol) tools to manage the TENETAIAGENCY101™ engines, Kubernetes deployments, Docker containers, and Kaggle submissions.

## Files

### 1. mcp-config.json
Basic MCP server configuration for Docker and Kubernetes integration.

```bash
# Enable in your MCP-compatible tool
export MCP_CONFIG="$(pwd)/mcp-config.json"
```

### 2. mcp-config-advanced.json
Advanced configuration with full tool definitions and security settings.

```bash
# Use with Claude, Cursor, or other MCP clients
export MCP_CONFIG="$(pwd)/mcp-config-advanced.json"
```

### 3. mcp_engine_manager.py
Python MCP server that provides 14 tools for engine management:

```bash
# Run as standalone MCP server
python3 mcp_engine_manager.py

# Or as part of MCP gateway
mcp-gateway --config mcp-config-advanced.json
```

## Available Tools

### Engine Management

#### engine_status
Get real-time status of all 3 engines.
```
Input: { "container": "all" | "engine-365-days" | "ultimate-engine" | "tenetaiagency-101" }
Output: Container status, uptime, health
```

#### engine_logs
Retrieve logs from engines with filtering.
```
Input: { "container": "engine-365-days", "tail": 100, "since": "10m" }
Output: Log lines with timestamps
```

#### engine_restart
Restart a specific engine container.
```
Input: { "container": "engine-365-days" }
Output: Restart confirmation
```

#### engine_stats
Get CPU, memory, and network statistics.
```
Input: { "container": "all" }
Output: Real-time resource usage
```

### Kubernetes Management

#### k8s_deploy
Deploy engines to Kubernetes cluster.
```
Input: { "namespace": "default" }
Output: Deployment status
```

#### k8s_status
Get Kubernetes pod and service status.
```
Input: { "namespace": "default" }
Output: Pod states, resource allocation
```

### Docker Compose Orchestration

#### docker_compose_up
Start the full stack locally.
```
Input: { "service": "all" }
Output: Container startup status
```

#### docker_compose_down
Stop the full stack.
```
Input: { "remove_volumes": false }
Output: Shutdown confirmation
```

### Kaggle Integration

#### kaggle_list_competitions
List active Kaggle competitions.
```
Input: { "limit": 20 }
Output: Competition list with details
```

#### kaggle_submit
Submit predictions from an engine to a competition.
```
Input: { "competition": "comp-ref", "engine": "engine-365-days", "message": "v1.0.0" }
Output: Submission confirmation
```

### Monitoring & Validation

#### consensus_check
Verify Byzantine consensus across all 3 engines.
```
Input: {}
Output: Consensus status (8/12 validators), k-value
```

#### audit_trail
Retrieve immutable SHA3-512 hash-linked audit trail.
```
Input: { "container": "all", "limit": 1000 }
Output: Audit records with timestamps and signatures
```

#### cycle_progress
Get 365-day cycle completion progress.
```
Input: {}
Output: Cycles completed, days remaining, progress %
```

## Setup Instructions

### 1. Install MCP Support
```bash
pip install mcp
```

### 2. Configure Your MCP Client

#### For Claude Desktop (macOS/Windows)
Edit `~/.config/claude/config.json`:
```json
{
  "mcpServers": {
    "engine-manager": {
      "command": "python3",
      "args": ["/path/to/mcp_engine_manager.py"]
    },
    "kubernetes": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "${HOME}/.kube:/root/.kube:ro",
        "-v", "/var/run/docker.sock:/var/run/docker.sock",
        "mcp/kubernetes:latest"
      ]
    }
  }
}
```

#### For Cursor
Edit `.cursor/mcp.json` in project root:
```json
{
  "mcpServers": {
    "engine-manager": {
      "command": "python3",
      "args": ["./mcp_engine_manager.py"]
    }
  }
}
```

#### For Terminal-based MCP Gateway
```bash
# Install MCP gateway
pip install mcp-gateway

# Start with config
mcp-gateway --config mcp-config-advanced.json
```

### 3. Verify Configuration

```bash
# Test engine status
python3 -c "from mcp_engine_manager import EngineManagerMCP; mcp = EngineManagerMCP(); print(mcp.execute_tool('engine_status', {}))"

# Test Docker connectivity
docker ps

# Test Kubernetes connectivity
kubectl get nodes
```

## Example MCP Commands

### Check All Engines
```
Use tool: engine_status
Parameters: { "container": "all" }
```

### Deploy to Kubernetes
```
Use tool: k8s_deploy
Parameters: { "namespace": "default" }
```

### Submit to Kaggle
```
Use tool: kaggle_submit
Parameters: {
  "competition": "some-competition",
  "engine": "ultimate-engine",
  "message": "v1.0.0 submission"
}
```

### Monitor 365-Day Progress
```
Use tool: cycle_progress
Parameters: {}
```

### Verify Byzantine Consensus
```
Use tool: consensus_check
Parameters: {}
```

## Security Considerations

1. **Environment Variables**: Keep KAGGLE_KEY in environment, not in code
2. **Docker Socket**: Only expose `/var/run/docker.sock` to trusted processes
3. **Kubeconfig**: Mount `.kube/config` as read-only
4. **API Credentials**: Use secure credential managers (AWS Secrets, Vault, etc.)

## Troubleshooting

### MCP Server Not Connecting
```bash
# Check if mcp_engine_manager.py is executable
chmod +x mcp_engine_manager.py

# Verify Python version (requires 3.8+)
python3 --version

# Test directly
python3 mcp_engine_manager.py
```

### Docker Socket Access Denied
```bash
# Ensure Docker daemon is running
docker ps

# Fix permissions (if needed)
sudo usermod -aG docker $USER
newgrp docker
```

### Kubernetes Cluster Unreachable
```bash
# Verify kubeconfig
kubectl config view

# Test connectivity
kubectl get nodes
```

## Integration with CI/CD

### GitHub Actions
```yaml
- name: Engine Status via MCP
  run: python3 mcp_engine_manager.py
  env:
    DOCKER_SOCKET: /var/run/docker.sock
    KAGGLE_KEY: ${{ secrets.KAGGLE_KEY }}
```

### GitLab CI
```yaml
engine_check:
  script:
    - python3 mcp_engine_manager.py
  environment:
    DOCKER_SOCKET: /var/run/docker.sock
```

## Support & Updates

For updates to this configuration, update the files and restart your MCP client.

All tools are versioned and backward-compatible.
