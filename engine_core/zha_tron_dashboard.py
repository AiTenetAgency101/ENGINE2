"""
ZHA + TRON Unified Dashboard API
Real-time monitoring and control of smart home automation
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json


class ZHATRONDashboardAPI:
    """REST API for ZHA + TRON orchestration"""

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.app = Flask(__name__)
        CORS(self.app)

        # Register routes
        self._register_routes()

    def _register_routes(self):
        """Register API endpoints"""

        @self.app.route("/api/health", methods=["GET"])
        def health():
            """Health check endpoint"""
            return (
                jsonify(
                    {
                        "status": "healthy",
                        "timestamp": datetime.now().isoformat(),
                        "version": "1.0.0",
                    }
                ),
                200,
            )

        @self.app.route("/api/status", methods=["GET"])
        def status():
            """Get complete system status"""
            return jsonify(self.orchestrator.get_orchestration_status()), 200

        @self.app.route("/api/tron/status", methods=["GET"])
        def tron_status():
            """Get TRON grid status"""
            return jsonify(self.orchestrator.tron_engine.get_grid_status()), 200

        @self.app.route("/api/zha/status", methods=["GET"])
        def zha_status():
            """Get ZHA integration status"""
            return jsonify(self.orchestrator.zha_integration.get_zha_status()), 200

        @self.app.route("/api/zha/devices", methods=["GET"])
        def zha_devices():
            """List all ZHA devices"""
            devices = {
                device_id: device.to_dict()
                for device_id, device in self.orchestrator.zha_integration.devices.items()
            }
            return (
                jsonify(
                    {
                        "total": len(devices),
                        "devices": devices,
                    }
                ),
                200,
            )

        @self.app.route("/api/zha/devices/<device_id>/state", methods=["GET"])
        def get_device_state(device_id):
            """Get specific device state"""
            device = self.orchestrator.zha_integration.devices.get(device_id)
            if not device:
                return jsonify({"error": "Device not found"}), 404

            return (
                jsonify(
                    {
                        "device_id": device_id,
                        "state": device.to_dict(),
                    }
                ),
                200,
            )

        @self.app.route("/api/zha/devices/<device_id>/control", methods=["POST"])
        def control_device(device_id):
            """Control a device"""
            data = request.json
            command = data.get("command")

            # Map command to state (simplified)
            from engine_core.zha_integration import ZHAState

            state_map = {"on": ZHAState.ON, "off": ZHAState.OFF}
            state = state_map.get(command)

            if not state:
                return jsonify({"error": "Invalid command"}), 400

            # Note: This would be async in production
            # For now, just update the device
            device = self.orchestrator.zha_integration.devices.get(device_id)
            if not device:
                return jsonify({"error": "Device not found"}), 404

            device.state = state

            return (
                jsonify(
                    {
                        "device_id": device_id,
                        "command": command,
                        "success": True,
                    }
                ),
                200,
            )

        @self.app.route("/api/zha/groups", methods=["GET"])
        def get_groups():
            """List device groups"""
            groups = {
                group_name: list(device_ids)
                for group_name, device_ids in self.orchestrator.zha_integration.device_groups.items()
            }
            return (
                jsonify(
                    {
                        "total": len(groups),
                        "groups": groups,
                    }
                ),
                200,
            )

        @self.app.route("/api/zha/groups/<group_name>/control", methods=["POST"])
        def control_group(group_name):
            """Control device group"""
            data = request.json
            command = data.get("command")

            # In production, this would be async
            if group_name not in self.orchestrator.zha_integration.device_groups:
                return jsonify({"error": "Group not found"}), 404

            group_devices = self.orchestrator.zha_integration.device_groups[group_name]

            return (
                jsonify(
                    {
                        "group": group_name,
                        "command": command,
                        "devices_targeted": len(group_devices),
                        "success": True,
                    }
                ),
                200,
            )

        @self.app.route("/api/scenes", methods=["GET"])
        def get_scenes():
            """List available scenes"""
            scenes = list(self.orchestrator.active_scenes.keys())
            return (
                jsonify(
                    {
                        "total": len(scenes),
                        "scenes": scenes,
                        "current_scene": self.orchestrator.current_scene,
                    }
                ),
                200,
            )

        @self.app.route("/api/scenes/<scene_name>/activate", methods=["POST"])
        def activate_scene(scene_name):
            """Activate a scene"""
            if scene_name not in self.orchestrator.active_scenes:
                return jsonify({"error": "Scene not found"}), 404

            # In production, this would be async
            actions = self.orchestrator.active_scenes[scene_name]

            return (
                jsonify(
                    {
                        "scene": scene_name,
                        "actions": len(actions),
                        "activated": True,
                        "timestamp": datetime.now().isoformat(),
                    }
                ),
                200,
            )

        @self.app.route("/api/automation/rules", methods=["GET"])
        def get_rules():
            """List automation rules"""
            if not hasattr(self.orchestrator, "automation_engine"):
                return jsonify({"total": 0, "rules": []}), 200

            rules = {
                rule_id: {
                    "name": rule.name,
                    "enabled": rule.enabled,
                    "executions": rule.execution_count,
                    "triggers": len(rule.triggers),
                    "actions": len(rule.actions),
                }
                for rule_id, rule in self.orchestrator.automation_engine.rules.items()
            }
            return (
                jsonify(
                    {
                        "total": len(rules),
                        "rules": rules,
                    }
                ),
                200,
            )

        @self.app.route("/api/metrics", methods=["GET"])
        def metrics():
            """Get system metrics"""
            return (
                jsonify(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "tron_cycles": self.orchestrator.metrics["total_cycles"],
                        "device_changes": self.orchestrator.metrics["device_changes"],
                        "total_devices": self.orchestrator.metrics["total_devices"],
                        "total_automations": self.orchestrator.metrics[
                            "total_automations"
                        ],
                        "energy_balance": self.orchestrator.tron_engine.energy_balance,
                        "sync_accuracy": self.orchestrator.tron_engine.sync_accuracy,
                        "grid_health": self.orchestrator.tron_engine.grid_health,
                    }
                ),
                200,
            )

        @self.app.route("/api/history/scenes", methods=["GET"])
        def scene_history():
            """Get scene execution history"""
            limit = request.args.get("limit", 50, type=int)
            history = self.orchestrator.scene_history[-limit:]

            return (
                jsonify(
                    {
                        "total": len(self.orchestrator.scene_history),
                        "recent": history,
                    }
                ),
                200,
            )

        @self.app.route("/api/history/state-changes", methods=["GET"])
        def state_history():
            """Get device state change history"""
            limit = request.args.get("limit", 100, type=int)
            history = self.orchestrator.zha_integration.state_history[-limit:]

            return (
                jsonify(
                    {
                        "total": len(self.orchestrator.zha_integration.state_history),
                        "recent": history,
                    }
                ),
                200,
            )

    def run(self, host="0.0.0.0", port=9000, debug=False):
        """Run the dashboard API"""
        print(f"\n[DASHBOARD] Starting ZHA + TRON Dashboard API")
        print(f"[DASHBOARD] Listening on http://{host}:{port}")
        print(f"[DASHBOARD] API Documentation:")
        print(f"  GET  /api/health             - Health check")
        print(f"  GET  /api/status             - Complete system status")
        print(f"  GET  /api/tron/status        - TRON grid status")
        print(f"  GET  /api/zha/status         - ZHA integration status")
        print(f"  GET  /api/zha/devices        - List all devices")
        print(f"  GET  /api/zha/devices/<id>/state    - Get device state")
        print(f"  POST /api/zha/devices/<id>/control  - Control device")
        print(f"  GET  /api/scenes             - List scenes")
        print(f"  POST /api/scenes/<name>/activate    - Activate scene")
        print(f"  GET  /api/metrics            - System metrics")
        print(f"  GET  /api/history/scenes     - Scene history")
        print(f"  GET  /api/history/state-changes - State change history")
        print(f"\n")

        self.app.run(host=host, port=port, debug=debug)


# HTML Dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>ZHA + TRON Unified Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 {
            text-align: center;
            color: white;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .card h2 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
        .metric:last-child { border-bottom: none; }
        .metric-label { font-weight: 600; color: #666; }
        .metric-value { color: #667eea; font-weight: bold; }
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }
        .status-healthy { background: #4caf50; color: white; }
        .status-warning { background: #ff9800; color: white; }
        .status-critical { background: #f44336; color: white; }
        .device-list { list-style: none; }
        .device-item {
            padding: 10px;
            margin: 5px 0;
            background: #f5f5f5;
            border-radius: 4px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .device-state { font-weight: bold; color: #667eea; }
        .progress-bar {
            width: 100%;
            height: 20px;
            background: #eee;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 5px;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
        }
        .timestamp {
            font-size: 0.9em;
            color: #999;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ ZHA + TRON Unified Dashboard</h1>
        
        <div class="grid" id="dashboard">
            <div class="card">
                <h2>System Status</h2>
                <div id="system-status">Loading...</div>
            </div>
            
            <div class="card">
                <h2>TRON Grid</h2>
                <div id="tron-status">Loading...</div>
            </div>
            
            <div class="card">
                <h2>ZHA Devices</h2>
                <div id="zha-status">Loading...</div>
            </div>
            
            <div class="card">
                <h2>Metrics</h2>
                <div id="metrics">Loading...</div>
            </div>
        </div>
    </div>
    
    <script>
        async function updateDashboard() {
            try {
                const status = await fetch('/api/status').then(r => r.json());
                const tron = await fetch('/api/tron/status').then(r => r.json());
                const zha = await fetch('/api/zha/status').then(r => r.json());
                const metrics = await fetch('/api/metrics').then(r => r.json());
                
                // Update system status
                const systemHtml = `
                    <div class="metric">
                        <span class="metric-label">Status</span>
                        <span class="status-badge status-healthy">OPERATIONAL</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Current Scene</span>
                        <span class="metric-value">${status.current_scene || 'None'}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Uptime</span>
                        <span class="metric-value">${status.tron.cycle} cycles</span>
                    </div>
                `;
                document.getElementById('system-status').innerHTML = systemHtml;
                
                // Update TRON status
                const tronHtml = `
                    <div class="metric">
                        <span class="metric-label">Cycle</span>
                        <span class="metric-value">${tron.cycle}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Nodes</span>
                        <span class="metric-value">${tron.nodes}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Sync Accuracy</span>
                        <span class="metric-value">${tron.sync_accuracy.toFixed(1)}%</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Energy</span>
                        <span class="metric-value">${tron.energy_balance.toFixed(1)}%</span>
                    </div>
                `;
                document.getElementById('tron-status').innerHTML = tronHtml;
                
                // Update ZHA status
                const zhaHtml = `
                    <div class="metric">
                        <span class="metric-label">Devices</span>
                        <span class="metric-value">${zha.total_devices}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Success Rate</span>
                        <span class="metric-value">${zha.success_rate.toFixed(1)}%</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Automations</span>
                        <span class="metric-value">${zha.automation_rules}</span>
                    </div>
                `;
                document.getElementById('zha-status').innerHTML = zhaHtml;
                
                // Update metrics
                const metricsHtml = `
                    <div class="metric">
                        <span class="metric-label">TRON Cycles</span>
                        <span class="metric-value">${metrics.tron_cycles}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Device Changes</span>
                        <span class="metric-value">${metrics.device_changes}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Grid Health</span>
                        <span class="metric-value">${metrics.sync_accuracy.toFixed(1)}%</span>
                    </div>
                `;
                document.getElementById('metrics').innerHTML = metricsHtml;
                
            } catch (error) {
                console.error('Error updating dashboard:', error);
            }
        }
        
        // Update every 5 seconds
        updateDashboard();
        setInterval(updateDashboard, 5000);
    </script>
</body>
</html>
"""


# Example usage
if __name__ == "__main__":
    from engine_core.zha_tron_orchestrator import ZHATRONOrchestrator

    # Create orchestrator
    orchestrator = ZHATRONOrchestrator()

    # Create and run dashboard
    dashboard = ZHATRONDashboardAPI(orchestrator)
    dashboard.run(host="0.0.0.0", port=9000, debug=False)
