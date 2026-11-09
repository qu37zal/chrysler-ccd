# Engineering rules

- Treat the vehicle bus as safety-critical. P0 capture is receive-only. If isolated-bench transmit stages are designed, keep them unpopulated and physically inhibited by a normally-open hardware link.
- Never connect to the vehicle until every used protocol-specific interface is high impedance, protected, and validated on a bench.
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
- P0 core is passive CCD capture on the Prowler's verified DLC pair. Other candidate contacts from ChryslerScanner V2.1.0 (PCI/VPW pin 2, SCI pins 6/7/9/12/14/15), full J1962 pass-through, and request/reply behavior are stretch goals. They are not verified for the Prowler's complete DLC population. Keep separate hardware and firmware threads for each later-confirmed bus/line; never collapse these physical layers into one front end.
- OEM service information describes CCD conductors around a 2.5 V common mode. Never assume 0/5 V line levels or add CCD bias/termination from a hobby schematic. Do not connect any candidate line to the ESP32 until its electrical envelope is established.
- Comparator and MOSFET parts in discussion are only candidates. Protection, threshold, hysteresis, loading, transmitter topology, and automotive power are not signed off. Keep CAD marked preliminary until the CCD front end and power path are bench-validated and reviewed; separately review any stretch channel before adding it.
- The ChryslerScanner and CCDBusTransceiver projects are GPL-3.0 references. Reuse their enclosure/connector ideas and cited facts, not their circuit artwork or code, unless license compatibility is reviewed.
- Local EDA tools found on this workstation: KiCad 10.0.7 CLI at `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe`; FreeRouting 2.5.0 at `%LOCALAPPDATA%\freerouting\freerouting.exe`. Check the existing install before downloading or reinstalling. Export/import through the project’s KiCad/FreeRouting handoff files and rerun KiCad DRC after importing routes.
- FreeRouting output is a routing proposal, not a manufacturing sign-off. Review the imported board in KiCad, inspect clearances and copper, run DRC, and keep unresolved electrical assumptions visible. Never fabricate or connect an unreviewed board to the vehicle.
