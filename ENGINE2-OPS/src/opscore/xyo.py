from hashlib import sha256
from datetime import datetime

def sign(payload: dict) -> str:
    data = (repr(sorted(payload.items())) + "|" + datetime.utcnow().isoformat()).encode("utf-8")
    return sha256(data).hexdigest()
