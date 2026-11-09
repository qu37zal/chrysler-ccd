# Chrysler CCD

Reusable platform for exploring Chrysler Collision Detection (CCD) networks, decoding vehicle events, and safely experimenting with isolated module emulation. Initial reference vehicle: 1999 Plymouth Prowler. P0 is a receive-only OBD-II sniffer; P1 is a reversible radio-interface controller. The project is designed to support research across Chrysler CCD-equipped vehicles, with vehicle-specific facts kept separate from shared protocol behavior.

## Safety status

This repository contains no authorized vehicle-bus transmitter. The firmware scaffold never transmits. CCD pins are DLC 3 (bus +) and 11 (bus -) per 1999 Prowler service-information pages. Do not connect a prototype until its high-impedance receive interface is bench-validated. Never add bus bias or termination without vehicle-specific evidence.

## Layout

- `firmware/p0-sniffer`: ESP32-S3 PlatformIO application scaffold; intended to host a local Wi-Fi AP and browser GUI.
- `lib/ccd`: transport-independent CCD frame and checksum/parser logic.
- `host`: Python capture parser, deterministic analysis/replay tools and a host-side relative autovolume controller model.
- `tests`, `fixtures`: synthetic-only protocol and analysis tests/captures.
- `docs`: requirements, safety procedures, architecture decisions, source inventory and hardware notes.
- `hardware/kicad/p0_carrier`: editable KiCad block schematic and routed carrier layout study for the ESP32-S3-DevKitC-1, J1962 pigtail header and future protected CCD receiver mezzanine. This is not a complete electrical interface or vehicle-ready PCB.
- `docs`: requirements, safety procedures, architecture decisions, source inventory and hardware notes.

## Milestones

1. **P0:** Capture every frame visible on the vehicle's CCD pair at the OBD-II DLC, with timestamps and error/loss metadata, then serve local status and logs over a device Wi-Fi AP/web GUI. This means all traffic observable on that pair, not every network or private module link in the vehicle.
2. **Bench emulation:** isolated virtual network and reviewed module behavior, with a reusable module-emulation interface. Initial candidates are OEM radio behavior and future CCD TPMS module/sensor emulation for newer sensors; each requires protocol discovery and isolated-bench validation. No vehicle transmission without explicit owner authorization.
3. **P1:** adapter-harness controller mapping validated BCM autovolume offset changes and steering events to measured resistor-multiplexed head-unit inputs, and decoded Reverse range to a protected 12 V camera-trigger output. The model sends relative volume steps; absolute head-unit volume is neither observed nor required. P0 remains the passive capture tool used to discover these signals.

## Host tooling

Python 3.10+; run `python -m unittest discover -s tests -v`. Synthetic fixture data is explicitly labeled and is not Prowler traffic. P0 includes a local Wi-Fi access point and browser GUI; Bluetooth and a native iOS app are later possibilities and are outside initial scope.

## Firmware

Build with PlatformIO (`pio run -d firmware/p0-sniffer`). Initial target is ESP32-S3 with a supported discrete CCD receiver and a future-capable, separate transmitter section kept unpopulated and physically inhibited in P0. Exact component selection, protection, pinout and bus loading remain open hardware decisions. USB serial and local AP/web capture interface are planned P0 transports.

## License

License selection is pending source/license audit. Do not copy GPL implementation code into this repository until a compatible project license is chosen. Documentation and independently written code remain separately attributable.
