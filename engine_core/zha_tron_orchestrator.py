"""
ZHA + TRON Unified Orchestration Engine
Synchronized smart home automation with distributed consensus
"""

import asyncio
from typing import Dict, List
from datetime import datetime
import json
from engine_core.tron_rhythm import TRONRhythmEngine
from engine_core.zha_integration import ZHAIntegration, ZHAState

class ZHATRONOrchestrator:
    """
    Unified ZHA + TRON Orchestration Engine
    Coordinates Zigbee devices with TRON rhythm synchronization
    """
    
    def __init__(self, node_id: str = "engine-orchestrator-1"):
        self.node_id = node_id
        self.tron_engine = TRONRhythmEngine(node_id=node_id, grid_frequency=0.2)
        self.zha_integration = ZHAIntegration(tron_engine=self.tron_engine)
        
        # Orchestration state
        self.active_scenes: Dict[str, List[Dict]] = {}
        self.current_scene: str = None
        self.scene_history: List[Dict] = []
        
        # Performance metrics
        self.metrics = {
            'total_cycles': 0,
            'total_devices': 0,
            'total_automations': 0,
            'sync_errors': 0,
            'automation_triggers': 0,
            'device_changes': 0,
        }

    async def initialize(self):
        """Initialize the orchestrator"""
        print("\n" + "="*70)
        print("ZHA + TRON UNIFIED ORCHESTRATION ENGINE")
        print("="*70)
        
        # Initialize TRON rhythm engine
        await self.tron_engine.initialize_grid()
        
        # Discover ZHA devices
        await self.zha_integration.discover_devices()
        
        # Register discovered devices with TRON
        for device_id in self.zha_integration.devices.keys():
            self.tron_engine.register_zha_device(device_id)
        
        self.metrics['total_devices'] = len(self.zha_integration.devices)

    async def create_scene(self, scene_name: str, actions: List[Dict]) -> bool:
        """Create a smart home scene"""
        self.active_scenes[scene_name] = actions
        print(f"\n[SCENE] Created scene: {scene_name}")
        print(f"  Actions: {len(actions)}")
        for action in actions:
            print(f"    • {action.get('device_id')}: {action.get('command')}")
        return True

    async def activate_scene(self, scene_name: str, sync_to_cycle: int = None) -> Dict:
        """Activate a smart home scene (synchronized with TRON)"""
        if scene_name not in self.active_scenes:
            return {'success': False, 'error': f'Scene {scene_name} not found'}
        
        actions = self.active_scenes[scene_name]
        self.current_scene = scene_name
        
        print(f"\n[ORCHESTRATOR] Activating scene: {scene_name}")
        print(f"  Synchronizing {len(actions)} device changes...")
        
        # Execute all actions (will be synchronized with TRON)
        execution_record = {
            'scene': scene_name,
            'timestamp': datetime.now().timestamp(),
            'actions': [],
            'sync_cycle': sync_to_cycle or self.tron_engine.current_cycle,
        }
        
        for action in actions:
            device_id = action.get('device_id')
            command = action.get('command')
            
            # Map command to state
            state_map = {
                'on': ZHAState.ON,
                'off': ZHAState.OFF,
            }
            
            new_state = state_map.get(command, ZHAState.UNKNOWN)
            
            if new_state != ZHAState.UNKNOWN:
                success = await self.zha_integration.set_device_state(
                    device_id,
                    new_state,
                    sync_cycle=execution_record['sync_cycle']
                )
                
                execution_record['actions'].append({
                    'device_id': device_id,
                    'command': command,
                    'success': success,
                })
        
        self.scene_history.append(execution_record)
        self.metrics['device_changes'] += len(actions)
        
        return {
            'success': True,
            'scene': scene_name,
            'actions_executed': len(execution_record['actions']),
            'sync_cycle': execution_record['sync_cycle'],
        }

    async def run_orchestration_cycle(self) -> Dict:
        """Run one complete ZHA + TRON orchestration cycle"""
        cycle_num = self.tron_engine.current_cycle
        
        print(f"\n{'='*70}")
        print(f"ORCHESTRATION CYCLE {cycle_num}")
        print(f"{'='*70}")
        
        # Prepare ZHA state
        zha_state = {
            'devices': {
                did: d.to_dict() 
                for did, d in self.zha_integration.devices.items()
            },
            'device_count': len(self.zha_integration.devices),
        }
        
        # Prepare TRON actions
        actions = []
        
        # Check if we have pending changes from ZHA
        pending_changes = []
        while not self.zha_integration.change_queue.empty():
            try:
                change = self.zha_integration.change_queue.get_nowait()
                pending_changes.append(change)
                actions.append({
                    'device': change['device_id'],
                    'command': 'sync',
                })
            except asyncio.QueueEmpty:
                break
        
        # Run TRON cycle (will execute all phases synchronized)
        await self.tron_engine.run_tron_cycle(zha_state, actions)
        
        # Sync ZHA with TRON
        zha_sync_result = await self.zha_integration.sync_with_tron(cycle_num)
        
        self.metrics['total_cycles'] += 1
        
        # Collect results
        cycle_result = {
            'cycle': cycle_num,
            'timestamp': datetime.now().isoformat(),
            'tron_phase': 'execution_complete',
            'zha_synced': zha_sync_result['synced'],
            'devices_updated': zha_sync_result['changes'],
            'tron_sync_accuracy': self.tron_engine.sync_accuracy,
            'grid_health': self.tron_engine.grid_health,
            'energy_balance': self.tron_engine.energy_balance,
        }
        
        return cycle_result

    def get_orchestration_status(self) -> Dict:
        """Get complete orchestration status"""
        tron_status = self.tron_engine.get_grid_status()
        zha_status = self.zha_integration.get_zha_status()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'node_id': self.node_id,
            'current_scene': self.current_scene,
            'tron': {
                'cycle': tron_status['cycle'],
                'nodes': tron_status['nodes'],
                'sync_accuracy': tron_status['sync_accuracy'],
                'consensus_efficiency': tron_status['consensus_efficiency'],
                'grid_health': tron_status['grid_health'],
                'energy_balance': tron_status['energy_balance'],
            },
            'zha': {
                'devices': zha_status['total_devices'],
                'devices_by_type': zha_status['devices_by_type'],
                'commands': zha_status['total_commands'],
                'success_rate': zha_status['success_rate'],
                'automation_rules': zha_status['automation_rules'],
                'device_groups': zha_status['device_groups'],
            },
            'metrics': self.metrics,
            'active_scenes': list(self.active_scenes.keys()),
            'scene_history': len(self.scene_history),
        }

    async def continuous_orchestration(self, cycles: int = 5):
        """Run continuous orchestration for N cycles"""
        await self.initialize()
        
        # Create some smart home scenes
        await self.create_scene("morning_routine", [
            {'device_id': 'light_living_room', 'command': 'on'},
            {'device_id': 'light_bedroom', 'command': 'off'},
            {'device_id': 'thermostat_bedroom', 'command': 'on'},
            {'device_id': 'lock_front_door', 'command': 'on'},
        ])
        
        await self.create_scene("evening_routine", [
            {'device_id': 'light_living_room', 'command': 'on'},
            {'device_id': 'light_bedroom', 'command': 'on'},
            {'device_id': 'thermostat_bedroom', 'command': 'on'},
            {'device_id': 'plug_kitchen', 'command': 'off'},
        ])
        
        await self.create_scene("away_mode", [
            {'device_id': 'light_living_room', 'command': 'off'},
            {'device_id': 'light_bedroom', 'command': 'off'},
            {'device_id': 'plug_kitchen', 'command': 'off'},
            {'device_id': 'lock_front_door', 'command': 'on'},
        ])
        
        # Activate a scene
        await self.activate_scene("morning_routine")
        
        # Run orchestration cycles
        for i in range(cycles):
            try:
                result = await self.run_orchestration_cycle()
                
                # Reactivate scene every 3 cycles for demonstration
                if i % 3 == 2:
                    await self.activate_scene("evening_routine")
                
                # Wait before next cycle
                await asyncio.sleep(1)
                
            except KeyboardInterrupt:
                print("\n[ORCHESTRATOR] Shutdown requested")
                break
            except Exception as e:
                print(f"[ERROR] {e}")
                await asyncio.sleep(1)
        
        # Print final status
        print(f"\n{'='*70}")
        print("FINAL ORCHESTRATION STATUS")
        print(f"{'='*70}")
        status = self.get_orchestration_status()
        print(json.dumps(status, indent=2))
        
        return status


# Example usage
if __name__ == "__main__":
    orchestrator = ZHATRONOrchestrator()
    asyncio.run(orchestrator.continuous_orchestration(cycles=5))
