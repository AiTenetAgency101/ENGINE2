"""
TRON Rhythm Engine - Synchronized Grid Protocol
Distributed consensus for ZHA devices with TRON cycles
"""

import asyncio
import time
from typing import Dict, List, Set
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import json
import hashlib


class TRONPhase(Enum):
    """TRON grid synchronization phases"""

    GRID_SYNC = "grid_sync"  # All nodes synchronize to master clock
    HEARTBEAT = "heartbeat"  # Distributed pulse across network
    COMMITMENT = "commitment"  # State commitment phase
    CONSENSUS = "consensus"  # Collective agreement phase
    EXECUTION = "execution"  # Synchronized action execution


@dataclass
class TRONPulse:
    """TRON synchronization pulse"""

    cycle_id: str
    timestamp: float
    phase: TRONPhase
    node_id: str
    grid_nonce: int
    energy_level: float  # 0-100%
    state_hash: str
    device_count: int


class TRONRhythmEngine:
    """
    TRON Rhythm Engine - Synchronized distributed consensus
    Coordinates ZHA devices in perfect grid synchronization
    """

    def __init__(self, node_id: str, grid_frequency: float = 0.1):
        self.node_id = node_id
        self.grid_frequency = grid_frequency  # Pulse frequency (Hz)
        self.cycle_duration = 1.0 / grid_frequency  # 10 seconds at 0.1Hz

        # Grid state
        self.current_cycle = 0
        self.grid_nonce = 0
        self.master_timestamp = 0.0
        self.nodes: Dict[str, Dict] = {}
        self.zha_devices: Set[str] = set()

        # TRON phases
        self.phase_timestamps = {phase: 0.0 for phase in TRONPhase}
        self.phase_allocations = {
            TRONPhase.GRID_SYNC: 0.02,  # 2s
            TRONPhase.HEARTBEAT: 0.02,  # 2s
            TRONPhase.COMMITMENT: 0.02,  # 2s
            TRONPhase.CONSENSUS: 0.02,  # 2s
            TRONPhase.EXECUTION: 0.02,  # 2s
        }

        # State tracking
        self.state_ledger: List[Dict] = []
        self.consensus_votes: Dict[str, Set[str]] = {}
        self.energy_balance = 100.0
        self.device_cache = {}

        # Metrics
        self.sync_accuracy = 100.0
        self.consensus_efficiency = 100.0
        self.grid_health = 100.0

    async def initialize_grid(self):
        """Initialize TRON grid synchronization"""
        self.master_timestamp = time.time()
        self.current_cycle = 0
        print(f"[TRON] Grid initialized at {self.master_timestamp}")
        print(f"[TRON] Cycle duration: {self.cycle_duration}s")
        print(f"[TRON] Frequency: {self.grid_frequency}Hz")

    async def grid_sync_phase(self):
        """Phase 1: Synchronize all nodes to master clock"""
        print(f"\n[TRON] Phase 1: GRID_SYNC (Cycle {self.current_cycle})")

        # Calculate time deviation for each node
        current_time = time.time()
        sync_offset = current_time - self.master_timestamp

        # Adjust master timestamp if drift detected
        if abs(sync_offset) > 0.001:  # >1ms drift
            self.master_timestamp += sync_offset * 0.5  # Gradual correction
            print(f"  ⚡ Corrected drift: {sync_offset*1000:.2f}ms")

        # Broadcast grid sync pulse
        nodes_synced = len(self.nodes) + 1  # +1 for self
        print(f"  ✓ Nodes synced: {nodes_synced}")
        print(f"  ✓ Sync accuracy: {self.sync_accuracy:.2f}%")

        self.phase_timestamps[TRONPhase.GRID_SYNC] = time.time()

    async def heartbeat_phase(self):
        """Phase 2: Distributed heartbeat across grid"""
        print(f"[TRON] Phase 2: HEARTBEAT")

        # Emit synchronized heartbeat
        heartbeat = {
            "cycle": self.current_cycle,
            "timestamp": time.time(),
            "node_id": self.node_id,
            "devices": len(self.zha_devices),
            "energy": self.energy_balance,
        }

        print(
            f"  💓 Heartbeat: Devices={heartbeat['devices']}, Energy={heartbeat['energy']:.1f}%"
        )

        # Update energy (decrease with device count)
        energy_drain = len(self.zha_devices) * 0.5
        self.energy_balance = max(0, self.energy_balance - energy_drain)

        self.phase_timestamps[TRONPhase.HEARTBEAT] = time.time()

    async def commitment_phase(self, zha_state: Dict):
        """Phase 3: Commit ZHA device states to ledger"""
        print(f"[TRON] Phase 3: COMMITMENT")

        # Create state commitment
        state_string = json.dumps(zha_state, sort_keys=True)
        state_hash = hashlib.sha256(state_string.encode()).hexdigest()[:16]

        commitment = {
            "cycle": self.current_cycle,
            "timestamp": time.time(),
            "state_hash": state_hash,
            "device_count": len(self.zha_devices),
            "committer": self.node_id,
        }

        self.state_ledger.append(commitment)
        print(f"  📝 State committed: {state_hash}")
        print(f"  📋 Ledger entries: {len(self.state_ledger)}")

        self.phase_timestamps[TRONPhase.COMMITMENT] = time.time()

    async def consensus_phase(self):
        """Phase 4: Achieve distributed consensus"""
        print(f"[TRON] Phase 4: CONSENSUS")

        # Consensus algorithm: >66% agreement required
        quorum = int(len(self.nodes) * 0.66) + 1

        # Simulate consensus voting
        consensus_key = f"cycle_{self.current_cycle}"
        votes = self.consensus_votes.get(consensus_key, set())
        votes.add(self.node_id)
        self.consensus_votes[consensus_key] = votes

        consensus_achieved = len(votes) >= quorum
        consensus_pct = (len(votes) / max(1, len(self.nodes) + 1)) * 100

        print(f"  🤝 Consensus votes: {len(votes)}/{len(self.nodes)+1}")
        print(f"  🤝 Consensus: {consensus_pct:.1f}%")

        if consensus_achieved:
            print(f"  ✓ Consensus ACHIEVED (>66%)")
            self.consensus_efficiency = min(100, self.consensus_efficiency + 0.5)
        else:
            print(f"  ✗ Consensus pending...")
            self.consensus_efficiency = max(50, self.consensus_efficiency - 0.5)

        self.phase_timestamps[TRONPhase.CONSENSUS] = time.time()

    async def execution_phase(self, actions: List[Dict]):
        """Phase 5: Execute synchronized actions"""
        print(f"[TRON] Phase 5: EXECUTION")

        if not actions:
            print(f"  ⏭️  No actions to execute")
            return

        print(f"  ⚙️  Executing {len(actions)} synchronized actions:")
        for action in actions:
            print(
                f"     • {action.get('device', 'unknown')}: {action.get('command', 'unknown')}"
            )

        # All actions execute within 1ms window (synchronized)
        execution_time = time.time()

        for action in actions:
            action["executed_at"] = execution_time
            action["cycle"] = self.current_cycle

        print(f"  ✓ All actions synchronized ({len(actions)} simultaneous)")

        self.phase_timestamps[TRONPhase.EXECUTION] = time.time()

    async def run_tron_cycle(self, zha_state: Dict = None, actions: List[Dict] = None):
        """Execute one complete TRON cycle"""
        cycle_start = time.time()

        print(f"\n{'='*60}")
        print(f"TRON CYCLE {self.current_cycle} START - {datetime.now().isoformat()}")
        print(f"{'='*60}")

        # Phase 1: Grid Sync
        await self.grid_sync_phase()
        await asyncio.sleep(self.phase_allocations[TRONPhase.GRID_SYNC])

        # Phase 2: Heartbeat
        await self.heartbeat_phase()
        await asyncio.sleep(self.phase_allocations[TRONPhase.HEARTBEAT])

        # Phase 3: Commitment
        if zha_state:
            await self.commitment_phase(zha_state)
        await asyncio.sleep(self.phase_allocations[TRONPhase.COMMITMENT])

        # Phase 4: Consensus
        await self.consensus_phase()
        await asyncio.sleep(self.phase_allocations[TRONPhase.CONSENSUS])

        # Phase 5: Execution
        if actions:
            await self.execution_phase(actions)
        await asyncio.sleep(self.phase_allocations[TRONPhase.EXECUTION])

        cycle_end = time.time()
        cycle_duration = cycle_end - cycle_start

        # Calculate metrics
        target_duration = self.cycle_duration
        accuracy = max(
            0, 100 - abs((cycle_duration - target_duration) / target_duration * 100)
        )
        self.sync_accuracy = accuracy

        print(f"\n[TRON] Cycle {self.current_cycle} complete")
        print(f"  ⏱️  Duration: {cycle_duration:.3f}s (target: {target_duration}s)")
        print(f"  📊 Sync Accuracy: {self.sync_accuracy:.2f}%")
        print(f"  🤝 Consensus Efficiency: {self.consensus_efficiency:.2f}%")
        print(f"  ⚡ Grid Health: {self.grid_health:.2f}%")
        print(f"  🔋 Energy: {self.energy_balance:.1f}%")

        self.current_cycle += 1
        self.grid_nonce += 1

    def register_zha_device(self, device_id: str):
        """Register ZHA device with TRON grid"""
        self.zha_devices.add(device_id)
        print(f"[ZHA] Registered device: {device_id}")
        print(f"[ZHA] Total devices: {len(self.zha_devices)}")

    def unregister_zha_device(self, device_id: str):
        """Unregister ZHA device from TRON grid"""
        self.zha_devices.discard(device_id)
        print(f"[ZHA] Unregistered device: {device_id}")

    def register_node(self, node_id: str):
        """Register grid node"""
        self.nodes[node_id] = {
            "joined_at": time.time(),
            "last_heartbeat": time.time(),
            "status": "active",
        }
        print(f"[GRID] Registered node: {node_id}")

    def get_grid_status(self) -> Dict:
        """Get complete grid status"""
        return {
            "cycle": self.current_cycle,
            "node_id": self.node_id,
            "nodes": len(self.nodes) + 1,
            "zha_devices": len(self.zha_devices),
            "sync_accuracy": self.sync_accuracy,
            "consensus_efficiency": self.consensus_efficiency,
            "grid_health": self.grid_health,
            "energy_balance": self.energy_balance,
            "state_ledger_entries": len(self.state_ledger),
            "master_timestamp": self.master_timestamp,
        }

    async def continuous_operation(self):
        """Run continuous TRON cycles"""
        await self.initialize_grid()

        cycle_count = 0
        while True:
            try:
                # Simulate ZHA device state
                zha_state = {
                    "devices": list(self.zha_devices),
                    "device_count": len(self.zha_devices),
                    "timestamp": time.time(),
                }

                # Simulate actions
                actions = []
                if len(self.zha_devices) > 0:
                    actions = [
                        {
                            "device": (
                                list(self.zha_devices)[0]
                                if self.zha_devices
                                else "none"
                            ),
                            "command": "sync",
                        }
                    ]

                # Run TRON cycle
                await self.run_tron_cycle(zha_state, actions)

                # Wait for next cycle
                await asyncio.sleep(max(0, self.cycle_duration - 0.1))

                cycle_count += 1
                if cycle_count >= 5:  # Run 5 cycles then stop for demo
                    break

            except KeyboardInterrupt:
                print("\n[TRON] Shutdown requested")
                break
            except Exception as e:
                print(f"[ERROR] {e}")
                await asyncio.sleep(1)


# Example usage
if __name__ == "__main__":
    engine = TRONRhythmEngine(node_id="engine-node-1", grid_frequency=0.1)

    # Register ZHA devices
    engine.register_zha_device("light_living_room")
    engine.register_zha_device("lock_front_door")
    engine.register_zha_device("thermostat_bedroom")

    # Register grid nodes
    engine.register_node("engine-node-2")
    engine.register_node("engine-node-3")

    # Run TRON cycles
    asyncio.run(engine.continuous_operation())

    # Print final status
    print(f"\n[STATUS] Final Grid Status:")
    status = engine.get_grid_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
