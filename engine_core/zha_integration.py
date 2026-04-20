"""
ZHA Integration Layer - Zigbee Home Automation + TRON Rhythm
Real-time device management with synchronized state transitions
"""

import asyncio
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json


class ZHADeviceType(Enum):
    """ZHA device categories"""

    LIGHT = "light"
    SWITCH = "switch"
    LOCK = "lock"
    THERMOSTAT = "thermostat"
    SENSOR = "sensor"
    COVER = "cover"
    FAN = "fan"
    PLUG = "plug"


class ZHAState(Enum):
    """ZHA device states"""

    ON = "on"
    OFF = "off"
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    UNKNOWN = "unknown"


@dataclass
class ZHADevice:
    """ZHA device representation"""

    device_id: str
    device_type: ZHADeviceType
    name: str
    state: ZHAState = ZHAState.UNKNOWN
    state_changed_at: float = 0.0
    attributes: Dict = field(default_factory=dict)
    last_seen: float = 0.0
    battery_level: Optional[int] = None
    signal_strength: int = -100

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "id": self.device_id,
            "type": self.device_type.value,
            "name": self.name,
            "state": self.state.value,
            "state_changed_at": self.state_changed_at,
            "attributes": self.attributes,
            "last_seen": self.last_seen,
            "battery": self.battery_level,
            "signal": self.signal_strength,
        }


class ZHAIntegration:
    """
    ZHA Integration - Real-time Zigbee Home Automation
    Synchronized with TRON rhythm for atomic state changes
    """

    def __init__(self, tron_engine=None):
        self.tron_engine = tron_engine
        self.devices: Dict[str, ZHADevice] = {}
        self.device_groups: Dict[str, Set[str]] = {}
        self.automation_rules: Dict[str, Dict] = {}
        self.state_history: List[Dict] = []
        self.change_queue: asyncio.Queue = asyncio.Queue()

        # Metrics
        self.total_commands = 0
        self.successful_commands = 0
        self.failed_commands = 0
        self.avg_response_time = 0.0

    async def discover_devices(self) -> List[ZHADevice]:
        """Discover Zigbee devices"""
        print("[ZHA] Discovering Zigbee devices...")

        # Simulated device discovery
        discovered_devices = [
            ZHADevice(
                device_id="light_living_room",
                device_type=ZHADeviceType.LIGHT,
                name="Living Room Light",
                state=ZHAState.ON,
                battery_level=None,
                signal_strength=-65,
            ),
            ZHADevice(
                device_id="light_bedroom",
                device_type=ZHADeviceType.LIGHT,
                name="Bedroom Light",
                state=ZHAState.OFF,
                battery_level=None,
                signal_strength=-72,
            ),
            ZHADevice(
                device_id="lock_front_door",
                device_type=ZHADeviceType.LOCK,
                name="Front Door Lock",
                state=ZHAState.ON,
                battery_level=87,
                signal_strength=-58,
            ),
            ZHADevice(
                device_id="thermostat_bedroom",
                device_type=ZHADeviceType.THERMOSTAT,
                name="Bedroom Thermostat",
                state=ZHAState.IDLE,
                battery_level=None,
                signal_strength=-64,
                attributes={"temperature": 21.5, "humidity": 45},
            ),
            ZHADevice(
                device_id="sensor_motion_hallway",
                device_type=ZHADeviceType.SENSOR,
                name="Hallway Motion Sensor",
                state=ZHAState.IDLE,
                battery_level=92,
                signal_strength=-71,
                attributes={"motion_detected": False},
            ),
            ZHADevice(
                device_id="plug_kitchen",
                device_type=ZHADeviceType.PLUG,
                name="Kitchen Smart Plug",
                state=ZHAState.ON,
                battery_level=None,
                signal_strength=-68,
                attributes={"power": 150, "voltage": 230},
            ),
        ]

        # Register devices
        for device in discovered_devices:
            self.devices[device.device_id] = device
            print(f"  ✓ {device.name} ({device.device_type.value})")

        print(f"[ZHA] Discovered {len(discovered_devices)} devices")
        return discovered_devices

    async def set_device_state(
        self,
        device_id: str,
        new_state: ZHAState,
        attributes: Dict = None,
        sync_cycle: int = None,
    ) -> bool:
        """Set device state (synchronized with TRON cycle)"""

        if device_id not in self.devices:
            print(f"[ZHA] ✗ Device not found: {device_id}")
            self.failed_commands += 1
            return False

        device = self.devices[device_id]
        old_state = device.state

        # Update device state
        device.state = new_state
        device.state_changed_at = datetime.now().timestamp()
        device.last_seen = datetime.now().timestamp()

        if attributes:
            device.attributes.update(attributes)

        # Record state change
        change_record = {
            "device_id": device_id,
            "device_name": device.name,
            "old_state": old_state.value,
            "new_state": new_state.value,
            "timestamp": device.state_changed_at,
            "sync_cycle": sync_cycle,
            "attributes": device.attributes,
        }
        self.state_history.append(change_record)

        self.successful_commands += 1
        self.total_commands += 1

        print(f"[ZHA] {device.name}: {old_state.value} → {new_state.value}")

        # Queue for TRON processing
        await self.change_queue.put(change_record)

        return True

    async def get_device_state(self, device_id: str) -> Optional[ZHADevice]:
        """Get current device state"""
        return self.devices.get(device_id)

    def create_device_group(self, group_name: str, device_ids: List[str]) -> bool:
        """Create device group for synchronized control"""
        self.device_groups[group_name] = set(device_ids)
        print(f"[ZHA] Created group '{group_name}' with {len(device_ids)} devices")
        return True

    async def control_device_group(
        self, group_name: str, command: str, value: any = None
    ) -> Dict:
        """Control all devices in a group"""
        if group_name not in self.device_groups:
            return {"success": False, "error": "Group not found"}

        device_ids = self.device_groups[group_name]
        results = {}

        print(f"[ZHA] Controlling group '{group_name}' ({len(device_ids)} devices)")

        # Map command to state
        state_map = {
            "on": ZHAState.ON,
            "off": ZHAState.OFF,
            "toggle": None,  # Toggle current state
        }

        for device_id in device_ids:
            if device_id in self.devices:
                device = self.devices[device_id]

                if command == "toggle":
                    new_state = (
                        ZHAState.OFF if device.state == ZHAState.ON else ZHAState.ON
                    )
                else:
                    new_state = state_map.get(command, ZHAState.UNKNOWN)

                if new_state:
                    success = await self.set_device_state(device_id, new_state)
                    results[device_id] = {"success": success}

        return {
            "group": group_name,
            "command": command,
            "devices_targeted": len(device_ids),
            "devices_controlled": len(
                [r for r in results.values() if r.get("success")]
            ),
            "results": results,
        }

    async def create_automation(
        self, rule_name: str, trigger: Dict, actions: List[Dict]
    ) -> bool:
        """Create ZHA automation rule"""
        rule = {
            "name": rule_name,
            "trigger": trigger,
            "actions": actions,
            "created_at": datetime.now().timestamp(),
            "enabled": True,
            "execution_count": 0,
        }

        self.automation_rules[rule_name] = rule
        print(f"[ZHA] Created automation rule: {rule_name}")
        print(f"      Trigger: {trigger}")
        print(f"      Actions: {len(actions)}")

        return True

    async def process_automation_rules(self, trigger_data: Dict) -> List[Dict]:
        """Process automation rules and execute matching actions"""
        matched_actions = []

        for rule_name, rule in self.automation_rules.items():
            if not rule["enabled"]:
                continue

            # Check if trigger matches
            trigger = rule["trigger"]
            if trigger.get("device_id") == trigger_data.get("device_id"):
                if trigger.get("state") == trigger_data.get("state"):
                    # Execute actions
                    for action in rule["actions"]:
                        matched_actions.append(action)

                    rule["execution_count"] += 1
                    print(
                        f"[ZHA] Automation triggered: {rule_name} ({rule['execution_count']} times)"
                    )

        return matched_actions

    def get_zha_status(self) -> Dict:
        """Get complete ZHA integration status"""
        device_states = {}
        by_type = {}

        for device_id, device in self.devices.items():
            device_states[device_id] = device.to_dict()

            dtype = device.device_type.value
            if dtype not in by_type:
                by_type[dtype] = 0
            by_type[dtype] += 1

        success_rate = (
            (self.successful_commands / self.total_commands * 100)
            if self.total_commands > 0
            else 0
        )

        return {
            "total_devices": len(self.devices),
            "devices_by_type": by_type,
            "device_states": device_states,
            "total_commands": self.total_commands,
            "successful_commands": self.successful_commands,
            "failed_commands": self.failed_commands,
            "success_rate": success_rate,
            "automation_rules": len(self.automation_rules),
            "device_groups": len(self.device_groups),
            "state_history_entries": len(self.state_history),
        }

    async def sync_with_tron(self, tron_cycle: int) -> Dict:
        """Synchronize ZHA state with TRON cycle"""
        if not self.tron_engine:
            return {"synced": False, "reason": "No TRON engine"}

        # Get all pending changes
        pending_changes = []
        while not self.change_queue.empty():
            try:
                change = self.change_queue.get_nowait()
                pending_changes.append(change)
            except asyncio.QueueEmpty:
                break

        # Create state snapshot
        state_snapshot = {
            "cycle": tron_cycle,
            "timestamp": datetime.now().timestamp(),
            "devices": {did: d.to_dict() for did, d in self.devices.items()},
            "pending_changes": pending_changes,
        }

        print(
            f"[ZHA-TRON] Syncing {len(pending_changes)} changes with cycle {tron_cycle}"
        )

        return {
            "synced": True,
            "cycle": tron_cycle,
            "changes": len(pending_changes),
            "devices": len(self.devices),
        }


# Example usage
if __name__ == "__main__":

    async def demo():
        # Initialize ZHA
        zha = ZHAIntegration()

        # Discover devices
        await zha.discover_devices()

        # Create device group
        zha.create_device_group("living_room", ["light_living_room", "plug_kitchen"])

        # Create automation rule
        await zha.create_automation(
            "motion_lights",
            trigger={"device_id": "sensor_motion_hallway", "state": "motion_detected"},
            actions=[
                {"device_id": "light_living_room", "command": "on"},
                {"device_id": "light_bedroom", "command": "on"},
            ],
        )

        # Simulate device control
        await zha.set_device_state("light_living_room", ZHAState.ON)
        await zha.set_device_state(
            "thermostat_bedroom", ZHAState.IDLE, {"temperature": 22.0}
        )

        # Control group
        result = await zha.control_device_group("living_room", "off")
        print(f"\n[ZHA] Group control result: {json.dumps(result, indent=2)}")

        # Print status
        status = zha.get_zha_status()
        print(f"\n[ZHA] Status:")
        print(f"  Devices: {status['total_devices']}")
        print(
            f"  Commands: {status['total_commands']} ({status['success_rate']:.1f}% success)"
        )
        print(f"  Automations: {status['automation_rules']}")
        print(f"  Groups: {status['device_groups']}")

    asyncio.run(demo())
