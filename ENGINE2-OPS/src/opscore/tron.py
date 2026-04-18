from ..inv.invariants import KAPREKAR

def tron_step(n: int) -> int:
    s = f"{n:04d}"
    high = int("".join(sorted(s, reverse=True)))
    low = int("".join(sorted(s)))
    return high - low

def tron_run(n: int, max_steps: int = 20):
    history = []
    current = n
    for _ in range(max_steps):
        nxt = tron_step(current)
        history.append((current, nxt))
        if nxt == current:
            break
        current = nxt
    converged_to = current if current == KAPREKAR else None
    return {
        "start": n,
        "history": history,
        "final": current,
        "converged_to": converged_to,
    }
