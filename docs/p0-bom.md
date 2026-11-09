# P0 parts selection

Updated 2026-11-09. The CCD subsystem now has a connected native KiCad schematic,
25 fitted components and a 14-line grouped bench purchase list. These are not
the complete board BOM or a fabrication release.

- [Selected components and exact orderables](../hardware/kicad/p0_frontend/components.json)
- [DigiKey / Mouser purchase exports and instructions](../hardware/bom/README.md)
- [Connected schematic and rebuild/check procedure](../hardware/kicad/p0_frontend/README.md)
- [SPICE fixtures, results and limits](../simulation/README.md)

## Selected CCD bench parts

| Function | Selection | Qty |
|---|---|---:|
| Differential receive | LT1716HS5#TRMPBF at 3.3 V | 1 |
| P-channel drive | BSS84Q-7-F | 1 |
| N-channel drive / gate control | 2N7002Q-7-F | 2 |
| Gate level shift | MMBT3906-7-F | 1 |
| Blocking / negative clamps | BAV21W-7-F | 4 |
| Input filter | 47 kOhm / 22 pF per conductor | 2 pairs |
| Drive limiting | 360 Ohm per branch | 2 |
| TX inhibit | TSW-102-07-G-S header; shunt absent for P0 | 1 |
| Other passives | Exact values/orderables in component inventory and CSVs | 9 |

The owner authorized populated, connected TX hardware with a removable inhibit.
P0 firmware stays receive-only; vehicle transmission is not authorized. No onboard
CCD bias or termination is fitted. Bench bias/load parts exist only in simulation.

LT1716 supersedes the earlier TLV3212-Q1/TLV1701 candidates because it tolerates
inputs above its own supply. Positive clamps into local rails are rejected: they
can load an unpowered tap. Ground-referenced positive transient protection and
input-resistor fault ratings remain open. Generic H-grade LT1716 is a 125 C part;
automotive #W qualification belongs to a different orderable. The family model
is not evidence of either qualification.

## Remaining board selections

| Block | Leading choice | Remaining work |
|---|---|---|
| Buck | LM5164QDDARQ1, 100 V / 1 A | Vendor model passes in LTspice, fails in ngspice; complete protected power path and rail optimization remain. |
| Inductor | Coilcraft MSS1246T-683MLB, 68 uH | TI reference part; 170 mOhm DCR modeled; saturation, thermals and layout checks remain. |
| 3.3 V LDO | TLV76701DGNR | Load-step model passed; thermal copper and full supply chain remain. |
| Fuse | Littelfuse 0451001.MRL candidate | Inrush and protection coordination. |
| Reverse battery / supply OR | Rated Schottky devices, orderables pending | USB/vehicle backfeed and startup/fault model. |
| Input transient clamp | SMBJ33A class candidate | Energy, source impedance and fuse coordination; no load-dump qualification claimed. |
| MCU | ESP32-S3; compact module option under review | Existing DevKit remains useful for bench work. Final footprint/power integration pending. |
| USB | Native S3 USB with Type-C / ESD | GCT USB4105 footprint family available; exact orderable and height pending. Two separate 5.1 kOhm CC resistors required. |

## OBD connector

The delegated purchasable sample candidate is Renhotec BSA-OBDM-R, seller MPN
id-561910452708, [listed in stock by Metabee](https://www.metabee.com/product-detail/obd2-16pin-male-gold-plated-connector-with-right_8777).
Its title says right angle while its attributes say straight. A full drawing or
measured sample is needed before releasing the footprint. No purchase/inquiry sent.

[Macchina CCBDM20](https://www.macchina.cc/catalog/parts/obd2-male-right-angle-pth-connector)
has drawing/STEP data but shows Notify Me. Drawing: 4 mm pin pitch, 2.65 mm PCB-tail
row spacing, not a generic 2.54 mm header. The upstream OBD2-90 is a footprint name,
not a supplier part number. [SparkFun DEV-09911](https://www.sparkfun.com/obd-ii-connector.html)
is purchasable but inspected photos show solder tabs/cups, suitable for a short-wire
case-mounted fallback rather than the requested PCB-tail connector.

## Scope and reference clues

Saved 2000 radio wiring traces CCD to DLC 3/11. Vet cavity view/orientation,
grounds and power before installation. Elvira is a 2000; archived 1999 literature
is a working carryover reference. PCI/VPW 2 and SCI 6/7/9/12/14/15 remain separate,
unverified stretch candidates and are excluded from this core purchase list.

ChryslerScanner's BOM includes SS34, LM2576S-5.0, ESDCAN24-2BLY, AO3400/AO3401,
IRF7317, 74HC4066, USBLC6-2SC6 and LM393D. CCDBusTransceiver V1.03 shows differential
receive and complementary drive through 360 Ohm branches. Their GPL-3.0 artwork
and code are not copied. The independent design does not adopt their switched
bias/termination or heavy direct bus capacitance. No obsolete IRF7317 or proprietary
4632650 is selected. The old p0_carrier is superseded and not a complete P0 board.
