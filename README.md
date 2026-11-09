# Chrysler CCD

Reusable platform for exploring Chrysler Collision Detection (CCD) networks, decoding vehicle events, and safely experimenting with isolated module emulation. Initial reference vehicle: 1999 Plymouth Prowler. P0 is a receive-only OBD-II sniffer; P1 is a reversible radio-interface controller. The project is designed to support research across Chrysler CCD-equipped vehicles, with vehicle-specific facts kept separate from shared protocol behavior.

## Safety status

P0's core target is a passive CCD capture from the verified Prowler DLC pair. Other DLC physical layers and full OBD-II tool behavior are stretch work. Candidate contacts from the ChryslerScanner reference include PCI/VPW (2) and SCI (6/7/9/12/14/15); these are not yet verified against the Prowler's complete DLC population. Keep the capture format extensible to separate protocol threads. P0 does not transmit. Do not connect an unvalidated prototype; never add CCD bias or termination without vehicle-specific evidence.

## Layout

- `firmware/p0-sniffer`: ESP32-S3 PlatformIO application scaffold; intended to host a local Wi-Fi AP and browser GUI.
- `lib/ccd`: transport-independent CCD frame and checksum/parser logic.
- `host`: Python capture parser, deterministic analysis/replay tools and a host-side relative autovolume controller model.
- `tests`, `fixtures`: synthetic-only protocol and analysis tests/captures.
- `docs`: requirements, safety procedures, architecture decisions, source inventory and hardware notes.
- `config/p0_threads.json`: machine-readable core CCD thread and stretch candidate DLC thread map. Candidate non-CCD contacts remain unverified for the Prowler.
- `hardware/kicad/p0_carrier`: earlier editable carrier/layout study for the ESP32-S3-DevKitC-1. It uses a generic pigtail header and has no bus receiver circuit; it is superseded by the CCD-core P0 plan in `docs/p0-bom.md` and ADR 0004. It is not a complete electrical interface or vehicle-ready PCB.
- `docs`: requirements, safety procedures, architecture decisions, source inventory and hardware notes.

## Milestones

1. **P0 core:** Obtain a genuine, timestamped, receive-only capture of Prowler CCD at the OBD-II port, with raw-frame/error/loss metadata and local Wi-Fi/USB access. The first web view can use one CCD tab.
2. **P0 stretch:** Add independently protected receiver threads for any other populated DLC protocol and a full OBD-II pass-through/sniffing mode if needed. The DLC does not expose every network or private module link in the vehicle. Active diagnostic requests and replies are later scope, not required for the first capture.
3. **Bench emulation:** isolated virtual network and reviewed module behavior, with a reusable module-emulation interface. Initial candidates are OEM radio behavior and future CCD TPMS module/sensor emulation for newer sensors; each requires protocol discovery and isolated-bench validation. No vehicle transmission without explicit owner authorization.
4. **P1:** adapter-harness controller mapping validated BCM autovolume offset changes and steering events to measured resistor-multiplexed head-unit inputs, and decoded Reverse range to a protected 12 V camera-trigger output. The model sends relative volume steps; absolute head-unit volume is neither observed nor required. P0 remains the passive capture tool used to discover these signals.

## Host tooling

Python 3.10+; run `python -m unittest discover -s tests -v`. Synthetic fixture data is explicitly labeled and is not Prowler traffic. P0 includes a local Wi-Fi access point and browser GUI; Bluetooth and a native iOS app are later possibilities and are outside initial scope.

## Firmware

Build with PlatformIO (`pio run -d firmware/p0-sniffer`). Initial target is ESP32-S3 with one CCD receive channel. USB serial and a local AP/web interface are the P0 transports. The capture record format carries a thread identifier so separately validated stretch channels can be added later. The current carrier board is superseded and must not be treated as the complete BOM or interface.

## License

License selection is pending source/license audit. Do not copy GPL implementation code into this repository until a compatible project license is chosen. Documentation and independently written code remain separately attributable.
