def tron_step(n: int) -> int:
    s = f"{n:04d}"
    high = int("".join(sorted(s, reverse=True)))
    low = int("".join(sorted(s)))
    return high - low

def run(payload):
    n = payload["n"]
    history = []
    current = n
    for _ in range(20):
        nxt = tron_step(current)
        history.append((current, nxt))
        if nxt == current:
            break
        current = nxt
    return {
        "engine": "TRON",
        "start": n,
        "history": history,
        "final": current
    }
