"""Strict JSON Lines capture reader/writer for decoded raw CCD frames."""
import json

def read_capture(stream):
    for number, line in enumerate(stream, 1):
        if not line.strip():
            continue
        item = json.loads(line)
        if item.get("type") != "frame":
            continue
        raw = bytes.fromhex(item["data"])
        if not raw:
            raise ValueError(f"line {number}: empty frame")
        yield {"timestamp_us": int(item["timestamp_us"]), "data": raw,
               "checksum": item.get("checksum", "unknown"),
               "synthetic": bool(item.get("synthetic", False))}

def write_frame(frame):
    return json.dumps({"type": "frame", "timestamp_us": frame["timestamp_us"],
                       "data": frame["data"].hex(" "),
                       "checksum": frame.get("checksum", "unknown"),
                       "synthetic": frame.get("synthetic", False)},
                      separators=(",", ":"))
