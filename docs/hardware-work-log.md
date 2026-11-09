# Hardware work log

## 2026-11-09

- Resumed LTspice after owner cleared its first-run privacy dialog.
- Inspected reference transceiver PDFs, Macchina drawing/STEP and SparkFun photos.
  The actual connector tail geometry differs from a generic 2.54 mm header;
  SparkFun's tabs/cups are not the requested right-angle PCB connector.
- Selected a purchasable Renhotec sample candidate, retaining its inconsistent
  orientation listing as a mechanical hold rather than guessing its footprint.
- Built independent CCD gate-drive and receiver models. Rejected local-rail
  positive input clamps because an unpowered tap can load the vehicle network.
- Established LT1716 at 3.3 V as the leading receiver; retained prior TLV1701
  experiments with an explicit superseded label. Recorded generic-vs-automotive
  grade distinctions and vendor model naming/parameter limitations.
- Added a connected 25-component native KiCad subsystem. Exported-netlist check:
  57/57 component pins, 18 nets. KiCad ERC: 0 errors, 0 warnings. This is not the
  complete P0 protected board and does not produce fabrication files.
- Added grouped one-assembly DigiKey/Mouser CSVs (14 lines). Supply observations
  expose backorders/small inventories; no cart changes or purchases were made.
- LTspice nominal CCD, receiver and buck fixtures passed. Eight synthetic CCD
  supply/load/capacitance cases passed. The jumper test uses an open switch and
  floating drive rail with its actual bleed. LDO fixture passed in ngspice.
- Same buck model failed to regulate in ngspice. Preserved failed result, required
  explicit measurement bounds, and added regression checks preventing solver
  completion or missing measurements from becoming a passing report.
- Host tests: 16 pass. No physical measurements, vehicle connection, live TX,
  final PCB artwork or manufacturing release occurred in this cycle.
- Remaining design work: ground-referenced positive input protection and fault
  ratings; final full power protection and thermals; MCU/USB integration; exact
  connector footprint; complete PCB, FreeRouting/DRC and enclosure fit.
