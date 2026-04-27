#!/usr/bin/env python
"""Cycle-based health check. Verifies last cycle completed successfully."""

import sys
from pathlib import Path

HEALTH_STATE_FILE = Path("/tmp/engine_cycle_health")

def check_cycle_health() -> bool:
    """
    Verify last cycle completed without errors.
    
    Returns:
        True if cycle healthy, False otherwise
    """
    if not HEALTH_STATE_FILE.exists():
        return False
    
    try:
        state = HEALTH_STATE_FILE.read_text().strip()
        return state == "healthy"
    except Exception:
        return False

if __name__ == "__main__":
    if check_cycle_health():
        sys.exit(0)
    else:
        sys.exit(1)
