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

## Future isolated module emulation
- The software and hardware architecture leaves room for reviewed CCD module behavior beyond the radio, including investigation of a CCD TPMS module/sensor emulator for newer sensors.
- TPMS message formats, sensor enrollment/identity, timing, compatibility and receiver behavior remain unknown until sourced or measured.
- Any TPMS emulation begins on an isolated bench network with bounded, reviewed message behavior; it does not authorize transmission on a vehicle bus.

## Acceptance
No valid vehicle capture or decoded signal is claimed until backed by timestamped capture and repeatable stationary test. Safety and licensing reviews precede release.
