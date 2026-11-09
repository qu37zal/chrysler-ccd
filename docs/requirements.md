# Requirements and acceptance criteria

## P0
- Passive receiver threads for every verified, populated data conductor at the DLC: CCD pair, PCI/VPW, and separate SCI lines where present. Each thread must have an independent receive front end, edge timestamp source, loss counter, raw capture and UI tab.
- Keep CCD, PCI/VPW, and each SCI line electrically separate. No bus bias or termination. Any future transmit driver has a separate, normally-open physical inhibit and remains unpopulated in the P0 vehicle-capture assembly.
- Verify candidate DLC pin mappings and each interface's electrical envelope from 1999 Prowler service information and isolated bench measurement before vehicle hookup.
- Monotonic microsecond timestamp, raw bytes, checksum/framing status and loss counters exported over USB.
- Bounded buffering; watchdog-safe recovery; firmware build reproducible in PlatformIO.
- Web UI provides a tab per protocol/thread and a shared cross-thread timeline with thread-level filters. The tabs must not conceal dropped samples or synthetic provenance.
- Host parser accepts documented JSONL, rejects malformed input, and clearly preserves synthetic provenance.

## P1
- Adapter harness only; measured head-unit KEY input impedance, voltage, resistor ladder and timing documented.
- Treat a validated BCM autovolume offset level as a relative requested compensation, not an absolute head-unit volume target. The offset's message ID and encoding remain unverified until captured.
- Convert changes in requested compensation into bounded volume-up/down button pulses. Track only the automatic contribution this controller has commanded; do not estimate the head unit's absolute volume.
- Pass steering-wheel manual volume presses through independently. A missed/lost pulse may require the driver to trim volume manually; do not retry indefinitely or issue command storms.
- OFF means zero automatic compensation; LOW/HIGH follow the corresponding validated BCM offset behavior rather than duplicating a presumed factory speed curve. Speed remains available for correlation and plausibility checks.
- On loss of fresh offset data, stop automatic commands and hold the current commanded contribution. On reset with unknown head-unit state, inhibit automatic compensation until a confirmed head-unit power cycle or a separately validated re-baselining procedure.
- Decode transmission range from CCD and assert the Android head unit's reverse-camera trigger only for a fresh, valid Reverse state. Drive a measured head-unit trigger input with a protected high-side 12 V stage; default low on reset, invalid/stale bus data, parser error or loss of controller power.
- P0 vehicle capture may be used to discover P1 speed, BCM offset, steering and transmission signals. P0 remains an OBD-connected receive-only device and does not drive KEY inputs or a reverse-trigger output.
- P1 head-unit behavior is first tested with an adapter harness and bench supply; do not connect the controller output to original reverse-lamp wiring.
- Offline simulation covers rising/falling BCM offset levels during acceleration/deceleration, manual steering adjustments, dropped offset frames and output pulses, bus loss/recovery, resets, repeated transitions and pulse rate/offset bounds.

## Future isolated module emulation
- The software and hardware architecture leaves room for reviewed CCD module behavior beyond the radio, including investigation of a CCD TPMS module/sensor emulator for newer sensors.
- TPMS message formats, sensor enrollment/identity, timing, compatibility and receiver behavior remain unknown until sourced or measured.
- Any TPMS emulation begins on an isolated bench network with bounded, reviewed message behavior; it does not authorize transmission on a vehicle bus.

## Acceptance
No valid vehicle capture or decoded signal is claimed until backed by timestamped capture and repeatable stationary test. Safety and licensing reviews precede release.
