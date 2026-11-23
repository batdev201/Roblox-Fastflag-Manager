# language: python, file: src/auto_refresh.py
import time
from src.offset_sources import load_offsets

POLL_INTERVAL = 30
MAX_WAIT     = 15 * 60

def fetch_fresh_until_match(running_guid: str, log=print):
    deadline = time.time() + MAX_WAIT
    attempt = 0
    while time.time() < deadline:
        attempt += 1
        try:
            dump = load_offsets(force_refresh=True)
        except Exception as e:
            log(f"[refresh] attempt {attempt}: fetch failed: {e}")
            time.sleep(POLL_INTERVAL)
            continue
        if dump.guid == running_guid:
            log(f"[refresh] attempt {attempt}: matched {running_guid}")
            return dump
        log(f"[refresh] attempt {attempt}: dump={dump.guid} running={running_guid}")
        time.sleep(POLL_INTERVAL)
    raise TimeoutError(f"dumper did not catch up to {running_guid}")
