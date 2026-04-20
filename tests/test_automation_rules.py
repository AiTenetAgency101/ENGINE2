import asyncio
from datetime import datetime

from engine_core.automation_rules import (
    AutomationAction,
    AutomationRule,
    AutomationRulesEngine,
)


def test_automation_rule_condition_operators():
    rule = AutomationRule("r1", "rule")

    state = {
        "temp": 21,
        "mode": "auto-cool",
        "humidity": 55,
    }

    assert rule._evaluate_condition({"entity": "temp", "condition": "equals", "value": 21}, state)
    assert rule._evaluate_condition({"entity": "temp", "condition": "not_equals", "value": 20}, state)
    assert rule._evaluate_condition({"entity": "temp", "condition": "gt", "value": 20}, state)
    assert rule._evaluate_condition({"entity": "temp", "condition": "lt", "value": 22}, state)
    assert rule._evaluate_condition({"entity": "temp", "condition": "gte", "value": 21}, state)
    assert rule._evaluate_condition({"entity": "temp", "condition": "lte", "value": 21}, state)
    assert rule._evaluate_condition({"entity": "humidity", "condition": "in_range", "value": (50, 60)}, state)
    assert rule._evaluate_condition({"entity": "mode", "condition": "contains", "value": "cool"}, state)


def test_automation_rule_execution_guards_and_state_updates():
    rule = AutomationRule("r1", "rule")
    rule.cooldown = 30
    rule.last_trigger_time = datetime.now().timestamp()

    assert rule.can_execute() is False

    rule.cooldown = 0
    rule.enabled = False
    assert rule.can_execute() is False

    rule.enabled = True
    result = asyncio.run(rule.execute())

    assert result["rule_id"] == "r1"
    assert result["execution_count"] == 1
    assert rule.last_execution is not None


def test_should_execute_requires_all_conditions_to_pass():
    rule = AutomationRule("r2", "conditional")
    rule.add_condition({"entity": "door", "condition": "equals", "value": "locked"})
    rule.add_condition({"entity": "temp", "condition": "gt", "value": 20})

    assert rule.should_execute({"door": "locked", "temp": 22}) is True
    assert rule.should_execute({"door": "unlocked", "temp": 22}) is False


class DummyZHA:
    def __init__(self):
        self.calls = []

    async def set_device_state(self, device_id, state, sync_cycle=None):
        self.calls.append((device_id, state, sync_cycle))
        return True


def test_engine_evaluate_triggers_updates_counters():
    engine = AutomationRulesEngine()

    always = engine.create_rule("always", "Always")
    always.add_condition({"entity": "flag", "condition": "equals", "value": True})

    disabled = engine.create_rule("off", "Off")
    disabled.enabled = False

    matches = asyncio.run(engine.evaluate_triggers({"flag": True}))

    assert matches == ["always"]
    assert engine.total_triggers == 1
    assert engine.triggers_fired["always"] == 1


def test_engine_execute_rules_runs_actions_and_records_history():
    zha = DummyZHA()
    engine = AutomationRulesEngine(zha_integration=zha)

    rule = engine.create_rule("r3", "Action rule")
    rule.add_action(AutomationAction(device_id="light_1", service="turn_on", data={"state": "on"}))

    result = asyncio.run(engine.execute_rules(["r3"], sync_cycle=7))

    assert result["rules_executed"] == 1
    assert result["actions"] == 1
    assert result["results"][0]["success"] is True
    assert zha.calls == [("light_1", "on", 7)]

    status = engine.get_engine_status()
    assert status["total_automations"] == 1
    assert status["total_actions"] == 1
    assert status["execution_history"] == 1
    assert status["automations_executed"]["r3"] == 1
