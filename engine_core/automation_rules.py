"""
Intelligent Automation Rules Engine
TRON-synchronized smart home automation with conditions and triggers
"""

import asyncio
from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, time
import json


class TriggerType(Enum):
    """Automation trigger types"""

    DEVICE_STATE = "device_state"
    TIME = "time"
    SUN = "sun"
    CONDITION = "condition"
    NUMERIC = "numeric"


class Condition(Enum):
    """Comparison conditions"""

    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    GREATER_THAN = "gt"
    LESS_THAN = "lt"
    GREATER_EQUAL = "gte"
    LESS_EQUAL = "lte"
    IN_RANGE = "in_range"
    CONTAINS = "contains"


@dataclass
class AutomationTrigger:
    """Automation trigger definition"""

    trigger_type: TriggerType
    entity_id: str
    condition: Condition = None
    value: Any = None
    tolerance: float = 0.0
    description: str = ""


@dataclass
class AutomationAction:
    """Automation action definition"""

    device_id: str
    service: str  # "turn_on", "turn_off", "set", etc.
    data: Dict = None


class AutomationRule:
    """Single automation rule with conditions and actions"""

    def __init__(self, rule_id: str, name: str, description: str = ""):
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.triggers: List[AutomationTrigger] = []
        self.conditions: List[Dict] = []
        self.actions: List[AutomationAction] = []
        self.enabled = True
        self.execution_count = 0
        self.last_execution = None
        self.mode = "single"  # single, restart, queue, parallel
        self.cooldown = 0  # Seconds between executions
        self.last_trigger_time = 0

    def add_trigger(self, trigger: AutomationTrigger) -> "AutomationRule":
        """Add trigger to rule"""
        self.triggers.append(trigger)
        return self

    def add_condition(self, condition: Dict) -> "AutomationRule":
        """Add condition to rule"""
        self.conditions.append(condition)
        return self

    def add_action(self, action: AutomationAction) -> "AutomationRule":
        """Add action to rule"""
        self.actions.append(action)
        return self

    def can_execute(self) -> bool:
        """Check if rule can execute (cooldown, enabled, etc.)"""
        if not self.enabled:
            return False

        current_time = datetime.now().timestamp()
        if current_time - self.last_trigger_time < self.cooldown:
            return False

        return True

    def should_execute(self, trigger_state: Dict) -> bool:
        """Check if rule should execute based on trigger state"""
        if not self.can_execute():
            return False

        # Check all conditions
        for condition in self.conditions:
            if not self._evaluate_condition(condition, trigger_state):
                return False

        return True

    def _evaluate_condition(self, condition: Dict, state: Dict) -> bool:
        """Evaluate a single condition"""
        entity = condition.get("entity")
        operator = Condition(condition.get("condition", "equals"))
        value = condition.get("value")

        entity_value = state.get(entity)

        if operator == Condition.EQUALS:
            return entity_value == value
        elif operator == Condition.NOT_EQUALS:
            return entity_value != value
        elif operator == Condition.GREATER_THAN:
            return entity_value > value
        elif operator == Condition.LESS_THAN:
            return entity_value < value
        elif operator == Condition.GREATER_EQUAL:
            return entity_value >= value
        elif operator == Condition.LESS_EQUAL:
            return entity_value <= value
        elif operator == Condition.IN_RANGE:
            min_val, max_val = value
            return min_val <= entity_value <= max_val
        elif operator == Condition.CONTAINS:
            return value in str(entity_value)

        return True

    async def execute(self) -> Dict:
        """Execute the automation rule"""
        if not self.can_execute():
            return {"success": False, "reason": "Cooldown active or rule disabled"}

        self.execution_count += 1
        self.last_trigger_time = datetime.now().timestamp()
        self.last_execution = datetime.now().isoformat()

        return {
            "rule_id": self.rule_id,
            "rule_name": self.name,
            "execution_count": self.execution_count,
            "timestamp": self.last_execution,
            "actions": len(self.actions),
        }


class AutomationRulesEngine:
    """
    Intelligent Automation Rules Engine
    Manages smart home automation with TRON synchronization
    """

    def __init__(self, tron_engine=None, zha_integration=None):
        self.tron_engine = tron_engine
        self.zha_integration = zha_integration

        self.rules: Dict[str, AutomationRule] = {}
        self.rule_history: List[Dict] = []
        self.triggers_fired: Dict[str, int] = {}
        self.automations_executed: Dict[str, int] = {}

        # Engine metrics
        self.total_triggers = 0
        self.total_automations = 0
        self.total_actions = 0

    def create_rule(
        self, rule_id: str, name: str, description: str = ""
    ) -> AutomationRule:
        """Create a new automation rule"""
        rule = AutomationRule(rule_id, name, description)
        self.rules[rule_id] = rule
        print(f"[AUTOMATION] Created rule: {name} (ID: {rule_id})")
        return rule

    async def evaluate_triggers(self, trigger_state: Dict) -> List[str]:
        """Evaluate all triggers and return matching rule IDs"""
        matching_rules = []

        for rule_id, rule in self.rules.items():
            if not rule.enabled:
                continue

            # For simplicity, check if rule should execute
            if rule.should_execute(trigger_state):
                matching_rules.append(rule_id)
                self.total_triggers += 1

                if rule_id not in self.triggers_fired:
                    self.triggers_fired[rule_id] = 0
                self.triggers_fired[rule_id] += 1

        return matching_rules

    async def execute_rules(self, rule_ids: List[str], sync_cycle: int = None) -> Dict:
        """Execute specified rules (synchronized with TRON)"""
        execution_results = []

        for rule_id in rule_ids:
            if rule_id not in self.rules:
                continue

            rule = self.rules[rule_id]

            # Execute rule
            result = await rule.execute()

            # Execute actions
            for action in rule.actions:
                if self.zha_integration:
                    success = await self.zha_integration.set_device_state(
                        action.device_id,
                        action.data.get("state") if action.data else None,
                        sync_cycle=sync_cycle,
                    )

                    execution_results.append(
                        {
                            "rule_id": rule_id,
                            "device_id": action.device_id,
                            "service": action.service,
                            "success": success,
                            "sync_cycle": sync_cycle,
                        }
                    )

            self.total_automations += 1
            if rule_id not in self.automations_executed:
                self.automations_executed[rule_id] = 0
            self.automations_executed[rule_id] += 1

            print(f"[AUTOMATION] Executed rule: {rule.name}")

        # Record execution
        execution_record = {
            "timestamp": datetime.now().isoformat(),
            "rules_executed": len(rule_ids),
            "actions": len(execution_results),
            "sync_cycle": sync_cycle,
            "results": execution_results,
        }
        self.rule_history.append(execution_record)
        self.total_actions += len(execution_results)

        return {
            "rules_executed": len(rule_ids),
            "actions": len(execution_results),
            "results": execution_results,
        }

    def get_engine_status(self) -> Dict:
        """Get automation engine status"""
        return {
            "total_rules": len(self.rules),
            "enabled_rules": len([r for r in self.rules.values() if r.enabled]),
            "disabled_rules": len([r for r in self.rules.values() if not r.enabled]),
            "total_triggers": self.total_triggers,
            "total_automations": self.total_automations,
            "total_actions": self.total_actions,
            "triggers_fired": self.triggers_fired,
            "automations_executed": self.automations_executed,
            "execution_history": len(self.rule_history),
        }


# Example automation rules
async def setup_example_automations(
    engine: AutomationRulesEngine, zha: "ZHAIntegration"
):
    """Setup example automation rules"""

    # Rule 1: Morning routine when alarm goes off
    morning = engine.create_rule(
        "morning_routine", "Morning Routine", "Lights on, thermostat warm, coffee ready"
    )
    morning.add_trigger(
        AutomationTrigger(
            trigger_type=TriggerType.TIME,
            entity_id="alarm_bedroom",
            value="07:00:00",
            description="Trigger at 7 AM",
        )
    )
    morning.add_action(
        AutomationAction(
            device_id="light_living_room", service="turn_on", data={"brightness": 100}
        )
    )
    morning.add_action(
        AutomationAction(
            device_id="thermostat_bedroom",
            service="set_temperature",
            data={"temperature": 22},
        )
    )
    morning.add_action(
        AutomationAction(device_id="plug_kitchen", service="turn_on", data={})
    )

    # Rule 2: Motion detected = lights on
    motion = engine.create_rule(
        "motion_lights",
        "Motion Activated Lights",
        "Turn on lights when motion detected",
    )
    motion.add_trigger(
        AutomationTrigger(
            trigger_type=TriggerType.DEVICE_STATE,
            entity_id="sensor_motion_hallway",
            value="motion_detected",
        )
    )
    motion.cooldown = 30  # 30 seconds between triggers
    motion.add_action(
        AutomationAction(device_id="light_living_room", service="turn_on")
    )

    # Rule 3: Door unlocked after sunset
    night_mode = engine.create_rule(
        "night_mode", "Night Mode", "Lights on at sunset, security mode active"
    )
    night_mode.add_trigger(
        AutomationTrigger(trigger_type=TriggerType.SUN, entity_id="sun", value="sunset")
    )
    night_mode.add_condition(
        {"entity": "lock_front_door", "condition": "equals", "value": "locked"}
    )
    night_mode.add_action(
        AutomationAction(device_id="light_living_room", service="turn_on")
    )
    night_mode.add_action(
        AutomationAction(device_id="light_bedroom", service="turn_on")
    )

    # Rule 4: Temperature control
    temp_control = engine.create_rule(
        "temperature_control",
        "Automatic Temperature Control",
        "Maintain temperature within range",
    )
    temp_control.add_trigger(
        AutomationTrigger(
            trigger_type=TriggerType.NUMERIC,
            entity_id="thermostat_bedroom",
            condition=Condition.LESS_THAN,
            value=20,
        )
    )
    temp_control.cooldown = 300  # 5 minute cooldown
    temp_control.add_action(
        AutomationAction(
            device_id="thermostat_bedroom",
            service="set_temperature",
            data={"temperature": 22},
        )
    )

    print(f"[AUTOMATION] Setup {len(engine.rules)} example rules")

    return engine


# Example usage
if __name__ == "__main__":

    async def demo():
        engine = AutomationRulesEngine()

        # Setup example rules
        await setup_example_automations(engine, None)

        # Simulate trigger
        trigger_state = {
            "alarm_bedroom": "triggered",
            "lock_front_door": "locked",
            "thermostat_bedroom": 19.5,
        }

        # Evaluate triggers
        matching_rules = await engine.evaluate_triggers(trigger_state)
        print(f"\n[AUTOMATION] Matching rules: {matching_rules}")

        # Execute rules
        result = await engine.execute_rules(matching_rules, sync_cycle=0)

        # Print status
        status = engine.get_engine_status()
        print(f"\n[AUTOMATION] Engine Status:")
        print(json.dumps(status, indent=2))

    asyncio.run(demo())
