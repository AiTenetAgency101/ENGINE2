from src.opscore import zha, tron, xyo

def run(op_name: str, payload: dict) -> dict:
    if not zha.allow(op_name, payload):
        return {"status": "DENY", "reason": "ZHA_BLOCK"}

    intent_anchor = xyo.sign({"op": op_name, "payload": payload})

    if op_name == "tron_cycle":
        result = tron.tron_run(payload["n"])
    else:
        return {"status": "DENY", "reason": "UNKNOWN_OP"}

    if not zha.invariant_ok(op_name, payload, result):
        return {"status": "BREACH", "intent_anchor": intent_anchor, "result": result}

    result_anchor = xyo.sign(result)

    return {
        "status": "OK",
        "op": op_name,
        "payload": payload,
        "intent_anchor": intent_anchor,
        "result": result,
        "result_anchor": result_anchor,
    }
