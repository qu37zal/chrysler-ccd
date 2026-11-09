# Chrysler CCD

Reusable platform for exploring Chrysler Collision Detection (CCD) networks, decoding vehicle events, and safely experimenting with isolated module emulation. Initial reference vehicle: 1999 Plymouth Prowler. P0 is a receive-only OBD-II sniffer; P1 is a reversible radio-interface controller. The project is designed to support research across Chrysler CCD-equipped vehicles, with vehicle-specific facts kept separate from shared protocol behavior.

## Safety status

P0 is designed as a passive, multi-thread DLC logger. Candidate contacts from the ChryslerScanner reference include CCD (3/11), PCI/VPW (2), and SCI (6/7/9/12/14/15); these are not yet verified against the Prowler's complete DLC population. Each protocol/line must have a separate, protected receiver. The current firmware scaffold is not yet a multibus implementation. Any bench transmit circuitry must remain physically inhibited and unpopulated for vehicle capture. Do not connect an unvalidated prototype; never add CCD bias or termination without vehicle-specific evidence.

## Layout

- `firmware/p0-sniffer`: ESP32-S3 PlatformIO application scaffold; intended to host a local Wi-Fi AP and browser GUI.
- `lib/ccd`: transport-independent CCD frame and checksum/parser logic.
- `host`: Python capture parser, deterministic analysis/replay tools and a host-side relative autovolume controller model.
- `tests`, `fixtures`: synthetic-only protocol and analysis tests/captures.
- `docs`: requirements, safety procedures, architecture decisions, source inventory and hardware notes.
- `config/p0_threads.json`: machine-readable candidate DLC thread map and tabbed UI behavior. All thread contacts remain explicitly unverified for the Prowler until OEM docs/physical DLC inspection confirm them.
- `hardware/kicad/p0_carrier`: earlier editable carrier/layout study for the ESP32-S3-DevKitC-1. It uses a generic pigtail header and has no bus receiver circuit; it is superseded by the multi-thread P0 electrical architecture in `docs/p0-bom.md` and ADR 0004. It is not a complete electrical interface or vehicle-ready PCB.
- `docs`: requirements, safety procedures, architecture decisions, source inventory and hardware notes.

## Milestones

1. **P0:** Capture every verified, populated data conductor exposed at the OBD-II DLC: CCD, PCI/VPW, and individual SCI lines where present. Preserve separate timestamped threads with raw/error/loss metadata, then provide per-thread tabs and a combined timeline over the device Wi-Fi AP/web GUI. The DLC does not expose every network or private module link in the vehicle.
2. **Bench emulation:** isolated virtual network and reviewed module behavior, with a reusable module-emulation interface. Initial candidates are OEM radio behavior and future CCD TPMS module/sensor emulation for newer sensors; each requires protocol discovery and isolated-bench validation. No vehicle transmission without explicit owner authorization.
3. **P1:** adapter-harness controller mapping validated BCM autovolume offset changes and steering events to measured resistor-multiplexed head-unit inputs, and decoded Reverse range to a protected 12 V camera-trigger output. The model sends relative volume steps; absolute head-unit volume is neither observed nor required. P0 remains the passive capture tool used to discover these signals.

## Host tooling

Python 3.10+; run `python -m unittest discover -s tests -v`. Synthetic fixture data is explicitly labeled and is not Prowler traffic. P0 includes a local Wi-Fi access point and browser GUI; Bluetooth and a native iOS app are later possibilities and are outside initial scope.

## Firmware

Build with PlatformIO (`pio run -d firmware/p0-sniffer`). Initial target is ESP32-S3 with separate protocol-specific receive channels. USB serial and a local AP/web interface with per-thread tabs are the P0 transports. Hardware channel circuits, protection, pinout, power input and loading remain open decisions. The current carrier board is superseded and must not be treated as the complete BOM or interface.

## License

License selection is pending source/license audit. Do not copy GPL implementation code into this repository until a compatible project license is chosen. Documentation and independently written code remain separately attributable.
