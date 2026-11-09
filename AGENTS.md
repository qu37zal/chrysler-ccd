# Engineering rules

- Treat the vehicle bus as safety-critical. Default to receive-only and physically inhibit transmit.
- Never connect to the vehicle until the interface is high impedance, protected, and validated on a bench.
- No unverified bias, termination, frame identifiers, signal encodings, or radio behavior. Label confidence and cite evidence.
- Distinguish CCD from PCI/J1850 VPW; do not reuse physical layers or timings across them.
- Keep transport, framing, decoding, events, and outputs separate. Use bounded buffers and explicit state machines.
- Synthetic captures must carry a synthetic marker and must never be described as measured vehicle data.
- No vehicle transmission, diagnostic replay, or irreversible wiring changes without explicit user authorization.
- Preserve upstream licenses. Do not incorporate copyleft source without resolving compatibility.
- Use deterministic host tests for parsing and control behavior. Do not claim vehicle validation from host tests.
- Track unknowns as issues and retain provenance in `docs/sources.md` and the signal dictionary.

## Persistent project facts and CAD workflow

- P0 is a receive-only Chrysler CCD exploration device for a 1999 Plymouth Prowler. The first packaging concept is a J1962 male vehicle connector at one end and USB-C at the other; do not add a scan-tool pass-through without a deliberate scope change.
- Do not equate a 16-contact J1962 connector with coverage of every diagnostic protocol. CCD, SCI, and PCI/VPW are separate physical interfaces. Verify the 1999 Prowler DLC pin population before connecting any non-CCD pins.
- OEM service information describes the CCD conductors around a 2.5 V common mode. Never assume 0/5 V line levels or add bus bias/termination from a hobby schematic. P0 omits all bus transmit hardware.
- The TLV3212-Q1 is only a receive-front-end candidate. Protection, threshold, hysteresis, loading, and automotive power are not signed off. Keep CAD marked preliminary until the front end and power path are bench-validated and reviewed.
- The ChryslerScanner and CCDBusTransceiver projects are GPL-3.0 references. Reuse their enclosure/connector ideas and cited facts, not their circuit artwork or code, unless license compatibility is reviewed.
- Local EDA tools found on this workstation: KiCad 10.0.7 CLI at `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe`; FreeRouting 2.5.0 at `%LOCALAPPDATA%\freerouting\freerouting.exe`. Check the existing install before downloading or reinstalling. Export/import through the project’s KiCad/FreeRouting handoff files and rerun KiCad DRC after importing routes.
- FreeRouting output is a routing proposal, not a manufacturing sign-off. Review the imported board in KiCad, inspect clearances and copper, run DRC, and keep unresolved electrical assumptions visible. Never fabricate or connect an unreviewed board to the vehicle.
