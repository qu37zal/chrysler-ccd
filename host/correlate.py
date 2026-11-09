"""Deterministic event-window byte frequency comparison; no signal guesses."""
from collections import Counter

def byte_histogram(frames, start_us, end_us):
    counts = Counter()
    for f in frames:
        if start_us <= f["timestamp_us"] < end_us:
            for i, b in enumerate(f["data"]):
                counts[(len(f["data"]), i, b)] += 1
    return counts

def compare(before, after):
    return after - before
