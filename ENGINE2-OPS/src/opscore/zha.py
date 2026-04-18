from . import tron
from ..inv.invariants import INV, PHI

def allow(op_name: str, payload: dict) -> bool:
    if op_name == "tron_cycle":
        n = payload.get("n")
        if not isinstance(n, int) or n < 0 or n > 9999:
            return False
        return True
    return False

def invariant_ok(op_name: str, payload: dict, result: dict) -> bool:
    if op_name == "tron_cycle":
        converged = result.get("converged_to") == INV.kaprekar
        return converged
    if "num" in payload and "den" in payload and payload["den"]:
        ratio = payload["num"] / payload["den"]
        return INV.within_tol(ratio, PHI)
    return True
