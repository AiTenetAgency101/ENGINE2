from engines.ultimate.ultimate import run as run_ultimate
from engines.tenet.tenet import run as run_tenet
from engines.worker365.worker365 import run as run_worker
from engines.tron.tron import run as run_tron
from engines.zha.zha import run as run_zha
from engines.xyo.xyo import run as run_xyo

def run_engine(name, payload):
    if name == "ultimate": return run_ultimate(payload)
    if name == "tenet": return run_tenet(payload)
    if name == "worker365": return run_worker(payload)
    if name == "tron": return run_tron(payload)
    if name == "zha": return run_zha(payload)
    if name == "xyo": return run_xyo(payload)
    return {"error": "unknown engine"}
