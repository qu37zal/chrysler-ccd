"""Capture record validation for independent, timestamped DLC receive threads."""
from __future__ import annotations

import json
from typing import Iterable, TextIO


def read_records(stream: TextIO) -> Iterable[dict]:
    """Read JSONL bus records without guessing protocol meaning.

    Supported input records are `edge` (a raw sampled receiver transition),
    `frame` (a protocol parser result), and `drop` (bounded-buffer loss marker).
    `thread` is mandatory so data from distinct physical layers is never merged.
    """
    for number, line in enumerate(stream, 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
            if item.get("type") not in {"edge", "frame", "drop"}:
                continue
            thread = item["thread"]
            timestamp = int(item["timestamp_us"])
            if not isinstance(thread, str) or not thread:
                raise ValueError("empty thread")
            if timestamp < 0:
                raise ValueError("negative timestamp")
            if item["type"] == "edge":
                if not isinstance(item["level"], bool):
                    raise ValueError("edge level must be boolean")
            elif item["type"] == "frame":
                raw = bytes.fromhex(item["data"])
                if not raw:
                    raise ValueError("empty frame")
                item["data"] = raw
            elif int(item["count"]) < 1:
                raise ValueError("drop count must be positive")
            item["timestamp_us"] = timestamp
            item["synthetic"] = bool(item.get("synthetic", False))
            yield item
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise ValueError(f"line {number}: invalid multibus capture record: {exc}") from exc
