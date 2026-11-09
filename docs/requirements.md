# Requirements and acceptance criteria

## P0
- **Core:** receive-only capture of the verified Prowler CCD pair through the OBD-II DLC, with genuine timestamps, raw frames, checksum/error status, loss counters, USB export, and local Wi-Fi status/capture UI.
- Keep the P0 vehicle interface receive-only. Do not fit or enable transmit drivers, add bus bias, or add termination.
- **Stretch:** separately protected receive channels for other confirmed DLC lines, a full J1962 pass-through logger, and diagnostic request/reply capture. These are not required for first CCD capture. Each additional physical layer must have its own verified front end; no generic/shared interface.
- Verify the Prowler CCD pin mapping and electrical envelope from vehicle-specific service information and isolated bench measurement before vehicle hookup. Confirm any additional pins independently before adding them.
- Monotonic microsecond timestamp, raw bytes, checksum/framing status and loss counters exported over USB.
- Bounded buffering; watchdog-safe recovery; firmware build reproducible in PlatformIO.
- Core web UI shows CCD capture/status. When stretch channels are implemented, show one tab per enabled thread and a combined timeline; filtering must not conceal dropped samples or synthetic provenance.
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
