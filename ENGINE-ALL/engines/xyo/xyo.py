from hashlib import sha256
from datetime import datetime

def run(payload):
    anchor = sha256((repr(payload) + datetime.utcnow().isoformat()).encode()).hexdigest()
    return {
        "engine": "XYO",
        "anchor": anchor,
        "input": payload
    }
