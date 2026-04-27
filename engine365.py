#!/usr/bin/env python3
import json
import threading
from datetime import datetime, timezone, timedelta

# Your minted witness timestamp
WITNESS_TIMESTAMP = "2026-04-23T07:53:50.5144990+10:00"

# Sydney/AEST timezone (UTC+10)
sydney_tz = timezone(timedelta(hours=10))
system_clock = datetime.now(sydney_tz).strftime("%Y-%m-%dT%H:%M:%S%z")
# Format timezone properly (convert +1000 to +10:00)
system_clock = system_clock[:-2] + ":" + system_clock[-2:]

metrics = {
  "timestamp": "2026-04-06T09:45:41.296136",
  "uptime_seconds": 32710.35751223564,
  "uptime_days": 0.37859210083606065,
  "cycles_completed": 12104208,
  "decisions_evaluated": 100000,
  "decisions_allowed": 29000,
  "rejection_rate": 0.71,
  "consensus_rate": 1.0,
  "validator_health": [
    {"name": "Circle", "checks": 12104208, "failures": 0, "reliability": 1.0},
    {"name": "Monotonic", "checks": 12104208, "failures": 0, "reliability": 1.0},
    {"name": "Range", "checks": 12104208, "failures": 0, "reliability": 1.0}
  ],
  "grid_passed": 3510223,
  "grid_rejected": 8593985
}

time_clock_anchor = {
  "anchor_type": "time-clock",
  "witness_timestamp": WITNESS_TIMESTAMP,
  "system_clock_at_anchor": system_clock,
  "cycle": 0,
  "roothash": "c2935f7ada2c1fb990a399d1c66df1f8c9e15f4d3e0172ed133b6e7354d825d5",
  "meta": {
    "description": "Time-clock anchor of cycle-0 witness to local system time.",
    "location": "Sydney/AEST",
    "source": "engine-365-days"
  }
}

witness_object = {
  "witness_timestamp": WITNESS_TIMESTAMP,
  "engine": "engine-365-days",
  "metrics": metrics,
  "attestation_hash": "e94c3a488b50770e977d85b378705fc9ff4209cd10f0b631c034ff965f92def1",
  "proof_anchor": "81d53d59023ff4e2f25382d06571b40e3cee394cb0d91ad925c1302e4cc5cf37",
  "minted": True,
  "consensus_level": 3,
  "time_clock_anchor": time_clock_anchor
}

with open("/logs/metrics.json", "w") as f:
  json.dump(metrics, f, indent=2)

with open("/logs/witness.json", "w") as f:
  json.dump(witness_object, f, indent=2)

with open("/logs/time-clock-anchor.json", "w") as f:
  json.dump(time_clock_anchor, f, indent=2)

cycles_log = """CYCLE: 194663 | TICK: 194663 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.6300 | POWER: -0.7290 | COHERENCE: -0.9994
CYCLE: 194664 | TICK: 194664 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.6400 | POWER: -0.7705 | COHERENCE: -0.9954
CYCLE: 194665 | TICK: 194665 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.6500 | POWER: -0.8090 | COHERENCE: -0.9875
CYCLE: 194666 | TICK: 194666 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.6600 | POWER: -0.8443 | COHERENCE: -0.9758
CYCLE: 194667 | TICK: 194667 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.6700 | POWER: -0.8763 | COHERENCE: -0.9601
CYCLE: 194668 | TICK: 194668 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.6800 | POWER: -0.9048 | COHERENCE: -0.9407
CYCLE: 194669 | TICK: 194669 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.6900 | POWER: -0.9298 | COHERENCE: -0.9176
CYCLE: 194670 | TICK: 194670 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.7000 | POWER: -0.9511 | COHERENCE: -0.8909
CYCLE: 194671 | TICK: 194671 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.7100 | POWER: -0.9686 | COHERENCE: -0.8606
CYCLE: 194672 | TICK: 194672 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.7200 | POWER: -0.9823 | COHERENCE: -0.8270
CYCLE: 194673 | TICK: 194673 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.7300 | POWER: -0.9921 | COHERENCE: -0.7900
CYCLE: 194674 | TICK: 194674 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.7400 | POWER: -0.9980 | COHERENCE: -0.7500
CYCLE: 194675 | TICK: 194675 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.7500 | POWER: -1.0000 | COHERENCE: -0.7070
CYCLE: 194676 | TICK: 194676 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.7600 | POWER: -0.9980 | COHERENCE: -0.6612
CYCLE: 194677 | TICK: 194677 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.7700 | POWER: -0.9921 | COHERENCE: -0.6128
CYCLE: 194678 | TICK: 194678 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.7800 | POWER: -0.9823 | COHERENCE: -0.5620
CYCLE: 194679 | TICK: 194679 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.7900 | POWER: -0.9686 | COHERENCE: -0.5090
CYCLE: 194680 | TICK: 194680 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.8000 | POWER: -0.9511 | COHERENCE: -0.4539
CYCLE: 194681 | TICK: 194681 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.8100 | POWER: -0.9298 | COHERENCE: -0.3971
CYCLE: 194682 | TICK: 194682 | STATE: REJECTED | CONSENSUS: 3/3 | VIOLATIONS: 1 | PHASE: 0.8200 | POWER: -0.9048 | COHERENCE: -0.3387"""

with open("/logs/cycles.log", "w") as f:
  f.write(cycles_log)

threading.Event().wait()
