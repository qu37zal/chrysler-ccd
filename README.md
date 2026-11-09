# Chrysler CCD

Reusable platform for exploring Chrysler Collision Detection (CCD) networks, decoding vehicle events, and safely experimenting with isolated module emulation. Initial reference vehicle: 1999 Plymouth Prowler. P0 is a receive-only OBD-II sniffer; P1 is a reversible radio-interface controller. The project is designed to support research across Chrysler CCD-equipped vehicles, with vehicle-specific facts kept separate from shared protocol behavior.

## Safety status

This repository contains no authorized vehicle-bus transmitter. The firmware scaffold never transmits. CCD pins are DLC 3 (bus +) and 11 (bus -) per 1999 Prowler service-information pages. Do not connect a prototype until its high-impedance receive interface is bench-validated. Never add bus bias or termination without vehicle-specific evidence.

## Layout

- `firmware/p0-sniffer`: ESP32-S3 PlatformIO application scaffold; intended to host a local Wi-Fi AP and browser GUI.
- `lib/ccd`: transport-independent CCD frame and checksum/parser logic.
- `host`: Python capture parser, deterministic analysis and replay tools.
- `tests`, `fixtures`: synthetic-only protocol and analysis tests/captures.
- `docs`: requirements, safety procedures, architecture decisions, source inventory and hardware notes.
- `hardware`: preliminary interface notes and BOM; no production PCB pending verification.

## Milestones

1. **P0:** Capture every frame visible on the vehicle's CCD pair at the OBD-II DLC, with timestamps and error/loss metadata, then serve local status and logs over a device Wi-Fi AP/web GUI. This means all traffic observable on that pair, not every network or private module link in the vehicle.
2. **Bench emulation:** isolated virtual network and reviewed module behavior; no vehicle transmission without explicit owner authorization.
3. **P1:** adapter-harness controller mapping CCD events to validated resistor-multiplexed head-unit input, with bounded autovolume state machine.

## Host tooling

Python 3.10+; run `python -m unittest discover -s tests -v`. Synthetic fixture data is explicitly labeled and is not Prowler traffic. Bluetooth and a native iOS app are later possibilities and are outside initial scope.

## Firmware

Build with PlatformIO (`pio run -d firmware/p0-sniffer`). Initial target is ESP32-S3 with a qualified CCD transceiver receiver output; exact component, pinout and bus load remain open hardware decisions. USB serial is primary; wireless telemetry is deferred until capture integrity is established.

## License

License selection is pending source/license audit. Do not copy GPL implementation code into this repository until a compatible project license is chosen. Documentation and independently written code remain separately attributable.
