# CCD front-end circuit review

This native KiCad schematic implements the candidate receiver and a populated
bench transmitter. It replaces the former empty receiver/mezzanine concept for
this subsystem. It is **not the full P0 board** and has no fabrication outputs.

- U101: LT1716 at 3.3 V, differential inputs through 47 kΩ / 22 pF networks.
- D103/D104: negative input clamps to ground, not to a local positive supply.
  Positive transient protection and component fault ratings still require review.
- Q101/Q102: complementary bus drive through blocking diodes and 360 Ω resistors.
- Q103/Q104: 3.3 V control to 5 V gate drive, with default-off gate resistors.
- JP101: removable transmit-power jumper. Populate the header, omit the shunt for P0.
- No onboard bus bias or termination. Those exist only in synthetic test fixtures.

The named CCD_P / CCD_N / 5V / 3V3 / GND / CCD_RX / TX_DOM nets connect to the
eventual connector, power, and MCU sheets. Power flags state the external supply
assumption for subsystem ERC; they do not implement a supply.

## Rebuild and check

With Python and `sexpdata` installed:

```powershell
.venv-hardware\Scripts\python.exe hardware/tools/build_ccd_frontend.py
& 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe' sch export netlist hardware/kicad/p0_frontend/p0_frontend.kicad_sch -o hardware/kicad/p0_frontend/p0_frontend.net
.venv-hardware\Scripts\python.exe hardware/tools/verify_frontend.py
& 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe' sch erc hardware/kicad/p0_frontend/p0_frontend.kicad_sch -o hardware/kicad/p0_frontend/erc.txt
```

`build_ccd_frontend.py` is the current component/net source for this subsystem.
It generates the native editable schematic, local comparator symbol, component
inventory, and grouped purchase CSVs. Changes in KiCad must be reconciled back
into that source before regenerating. Installed KiCad library symbols are used
under their CC-BY-SA license with the KiCad library exception. Circuit design
and generation code are independently authored, not copied from upstream GPL
schematics.

The corresponding candidate circuit is `simulation/ccd_frontend_lt1716.lib`.
Family models do not establish temperature-grade, ESD, fault, or vehicle compliance.
