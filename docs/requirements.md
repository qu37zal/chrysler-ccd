# Requirements and acceptance criteria

## P0
- Physically transmit-inhibited CCD receiver; no bias or termination added.
- DLC 3/11 mapping and interface electrical envelope verified from 1999 Prowler documentation and bench measurement.
- Monotonic microsecond timestamp, raw bytes, checksum/framing status and loss counters exported over USB.
- Bounded buffering; watchdog-safe recovery; firmware build reproducible in PlatformIO.
- Host parser accepts documented JSONL, rejects malformed input, and clearly preserves synthetic provenance.

## P1
- Adapter harness only; measured head-unit KEY input impedance, voltage, resistor ladder and timing documented.
- Bounded volume compensation, three switch modes, hysteresis, smoothing, manual-change tracking, power-cycle recovery, passive failure behavior.
- Offline simulation covers speed transitions, manual adjustments, message loss and resets.

## Acceptance
No valid vehicle capture or decoded signal is claimed until backed by timestamped capture and repeatable stationary test. Safety and licensing reviews precede release.
