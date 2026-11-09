# P0 carrier layout study

**Status: superseded.** This artifact predates the decision to capture multiple independent DLC protocol threads. It has no J1962 board connector, power front end, or bus receiver/transmitter circuits. Do not use its PCB, DSN, SES, 3D preview, or schematic PDF as a P0 BOM or fabrication package. The current multi-thread hardware requirements and candidate BOM are in `docs/p0-bom.md`; the old board remains only as a KiCad/FreeRouting workflow example.

This KiCad project is a preliminary carrier for an ESP32-S3-DevKitC-1 and a future protected CCD receiver daughterboard. It is intentionally not a complete transceiver or vehicle-ready design.

## Layout proposal

- 88 x 38 mm two-layer carrier, subject to mechanical fit checks.
- 2x8 internal pigtail header at the J1962 end, with header pad numbers matching OBD connector pin numbers.
- Two 1x22 socket rows for the Espressif ESP32-S3-DevKitC-1 v1.1. Its USB-C connector faces the opposite end and exits through a case opening.
- 1x6 receiver mezzanine header: raw CCD candidate pair, local GND, 3V3, logic RX to DevKitC J1-4/GPIO4, and one reserved pad.
- DLC pins 3 and 11 are tentative CCD taps. The other DLC contacts remain unconnected in this layout study. Vehicle-specific pin mapping and front-end coverage are still open.
- DLC pin 16 is not connected to carrier power. This draft powers the DevKitC through USB-C; a protected 12 V input stage is future work.
- Vehicle signal ground is isolated from local logic ground by default. JP1 is an unpopulated optional link for later review after the Prowler pinout and front-end reference scheme are confirmed.

The carrier routes only the nets shown in its PCB and a small number of explicitly mapped DevKitC pins. The receiver mezzanine must provide validated input protection and threshold/hysteresis before any connection to the Prowler.

## Files and commands

`p0_carrier.kicad_sch` is a block-level engineering schematic and assumption register, not a component-level receiver circuit. `p0_carrier.kicad_pcb` is generated from `tools/build_carrier.py`. The script exports a Specctra DSN; FreeRouting routes the defined nets to a SES session; the script then imports that session back into KiCad and normalizes any router neckdowns to the 0.20 mm carrier signal width.

The current [3D fit preview](p0_carrier_3d.png) and [schematic PDF](p0_carrier_schematic.pdf) are visual aids only. The preview renders the carrier connectors, not the ESP32 DevKit itself, J1962 shell, or final enclosure.

On this workstation, KiCad CLI is `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe` and FreeRouting is `%LOCALAPPDATA%\freerouting\freerouting.exe` (v2.5.0). Run from this directory:

```powershell
& 'C:\Program Files\KiCad\10.0\bin\python.exe' .\tools\build_carrier.py
& "$env:LOCALAPPDATA\freerouting\freerouting.exe" -de .\p0_carrier.dsn -do .\p0_carrier.ses --router.autorouter.max_passes=10 -mt 8
& 'C:\Program Files\KiCad\10.0\bin\python.exe' .\tools\build_carrier.py --import-ses
& 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe' pcb drc .\p0_carrier.kicad_pcb -o .\drc.txt
```

Autorouting is only a routing proposal. Review the board in KiCad and resolve the electrical, mechanical, and DRC issues before fabrication. Do not connect an unreviewed board to the vehicle.
