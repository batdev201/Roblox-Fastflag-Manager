# language: python, file: src/apply_all.py
# Applies every flag present in the loaded dump, using dump default values.
# Curated overrides win. Known-bad flags are skipped with a reason.

from typing import Optional

BLOCKLIST = {
    "TaskSchedulerTargetFps": "memory-only on Hyperion; JSON path dead",
    "DFIntTaskSchedulerTargetFps": "memory-only on Hyperion",
    "FFlagDebugGraphicsDisableDirect3D11": "can hang client on launch",
    "FFlagDebugGraphicsPreferVulkan": "driver-dependent",
    "DFIntTextureQualityOverride": "out-of-range value corrupts textures",
}

CURATED = {
    "FIntCameraMaxZoomDistance": 400,
    "DFIntTaskSchedulerTargetFps": 240,
    "FFlagDebugGraphicsPreferD3D11": 1,
    "DFFlagDisableDPIScale": 1,
}

def apply_all(flag_manager, dump, guid_ok: bool) -> list[dict]:
    rows = []
    for f in dump:
        name = f["name"]
        if name in BLOCKLIST:
            rows.append({"name": name, "status": "SKIPPED", "detail": BLOCKLIST[name]})
            continue
        value = CURATED.get(name, f.get("default"))
        if value is None:
            rows.append({"name": name, "status": "MISSING", "detail": "no default"})
            continue
        if not guid_ok:
            rows.append({"name": name, "status": "SKIPPED_GUID", "detail": "guid mismatch"})
            continue
        try:
            ok = flag_manager.apply_memory(name, value)
            rows.append({"name": name, "status": "MEMORY" if ok else "READONLY", "detail": ""})
        except Exception as e:
            rows.append({"name": name, "status": "READONLY", "detail": str(e)[:60]})
    return rows
