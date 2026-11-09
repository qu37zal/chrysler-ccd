# P0 preliminary BOM and packaging concept

Status: prototype planning only; no vehicle-ready schematic, PCB, or enclosure released.

## Packaging direction

Use an OBD-II/J1962 male plug at the vehicle end and a USB-C device connector at the opposite end. Put the ESP32-S3 and receiver board in a compact serviceable enclosure that can be 3D printed after the chosen J1962 plug and USB connector are measured. The Chrysler Scanner V2.1.0 photos show a compact PCB inside a black enclosure with USB access and accessible power/debug points. Its later board is an integrated diagnostic tool; our packaging borrows the compact enclosed-board approach, not its circuit or transmit functions. The separate CCDBusTransceiver board is a useful scale reference at 33 x 25 x 12.4 mm, but that dimension excludes the OBD connector and does not set this enclosure size.

```text
vehicle DLC -- J1962 male -- [enclosure: protected taps + ESP32-S3 + status] -- USB-C -- computer
                                      +-- Wi-Fi AP / local capture GUI
```

This draft interprets the requested form as a plug-in dongle. It does not include a second, female scan-tool pass-through connector; adding one would substantially enlarge the case and needs a separate packaging decision. Every populated J1962 pin should be documented and assessed, but only confirmed, high-impedance receiver taps should connect to circuitry. The device is not electrically transparent to every protocol merely because its connector has 16 contacts.

## Preliminary parts list

| Ref. | Qty. | Candidate / description | Status and rationale |
|---|---:|---|---|
| U1 | 1 | ESP32-S3 module or DevKitC-1 for prototype | Selected platform. Native USB CDC avoids a separate USB-UART bridge; Wi-Fi AP and web UI run on the module. For first capture, use the dev board; later make a carrier PCB around a module after power, RF, and USB details are fixed. |
| J1 | 1 | J1962 16-contact male plug, board-mount or short pigtail style | Required mechanical interface. Exact part TBD from verified footprint, contact retention, cable/strain-relief, and enclosure dimensions. A pigtail eases a hobbyist prototype; board-mount is tidier but constrains the PCB and case. |
| J2 | 1 | USB-C receptacle, USB 2.0 device wiring | Opposite-end data/configuration connector. Select after deciding board-mounted versus cable/strain-relieved implementation. Include correct CC pull-downs if not already on the selected ESP32 board. |
| U6 | 1 | USB data-line ESD protection device | Add near exposed USB-C connector after selecting connector layout and checking USB 2.0 signal capacitance. Exact part TBD. |
| Rcc1/Rcc2 | 2 | USB-C CC pull-down resistors | Device-side Rd, nominal 5.1 kOhm to ground on CC1/CC2 when using a USB-C receptacle; omit duplicates if already present on the selected dev board/carrier. |
| U2 | 1 | TI TLV3212-Q1 dual comparator, e.g. SOIC-8 `TLV3212QDRQ1` | Receiver prototype candidate, not a CCD transceiver. 3.3 V supply/output and suitable common-mode range are promising; input protection, threshold, hysteresis, polarity, and loading still need a reviewed schematic and bench tests. Confirm live stock/package before ordering. |
| U3 | 1 | Automotive-rated protected buck regulator, 12 V to 5 V | Required if powered from J1962 pin 16. **Not selected** until quiescent/current budget, cranking, reverse battery, and transient envelope are set. Do not choose an ordinary 12 V-to-5 V hobby buck by input-voltage label alone. |
| F1 | 1 | Fuse or resettable protection in pin-16 power path | Required concept; rating and type TBD from power budget and harness strategy. |
| D1 / Q1 | 1 set | Reverse-polarity protection and surge clamp coordinated with U3 | Required concept; no part selected before power transient requirements and topology review. |
| U4 | 1 per distinct supported line layer | Receive-only physical front end(s) for confirmed DLC signals | CCD receiver candidate is U2. SCI or other diagnostic lines require separate, appropriate front ends after confirming 1999 Prowler DLC pin use and electrical levels. P0 claims broad available-port capture only after this inventory. |
| R/C/D | as designed | Input series impedance, bias/reference/hysteresis network, low-capacitance protection, local decoupling | Values and exact protection parts are deliberately open. Do not install bus bias or termination. Protect each monitored signal without placing a material load on the bus. |
| U5 / storage | 1 | Optional microSD socket/card or other capture storage | Not required for first live stream if web/USB export works. Add only if standalone capture without a connected client is needed; capture loss behavior and card power integrity need design. |
| LED1..n | 2-3 | Power, capture, and error/status LEDs | Useful for enclosed operation; keep functions documented and current limited. Wi-Fi/device state is visible in GUI as well. |
| TP1..n | several | Test pads for vehicle supply, protected 5 V, 3V3, GND, bus inputs, receiver output(s) | Add to the carrier PCB for bench debug; keep test access electrically safe and clearly labeled. |
| H1 | 1 | 3D-printed enclosure, internal PCB retention, connector strain relief | Prototype material and dimensions TBD. Measure actual mating plug, module/dev-board, USB plug shell and clearance, print tolerances, and under-dash access before CAD freeze. |

## Prototype phases

1. **Bench receiver:** ESP32-S3 dev board, one TLV3212-Q1 sample if available (and available parts-bin comparators for comparison), isolated low-voltage waveform source, current-limited lab supply, and test leads. Validate the receive concept off-vehicle. No transmitter, bus bias, or termination.
2. **Vehicle-power bench:** add the protected pin-16 power chain only after a candidate schematic has been checked against the regulator and protection data sheets. Validate current draw, startup, reverse protection, and supply transients using an appropriate lab setup.
3. **OBD prototype harness:** use a verified J1962 male plug. Confirm its pin map against the 1999 Prowler documentation and continuity-test the harness before insertion. Begin with only ground, protected power, and the proven high-impedance receiver taps connected.
4. **Enclosure:** model the selected connector, carrier/dev-board, USB access, strain relief, and cooling. Print a fit-check shell before finalizing the PCB outline.

## Known architecture clues from the reference hardware

- ChryslerScanner V2.1.0 schematic material lists an ESP32-PICO-D4, USBLC6-2SC6 USB protection, CP2102 USB-UART bridge, TS391C comparator, 74LVC2G66 switches, AO3400 MOSFETs, HSW4602 switches, and multiple interfaces for CCD, PCI/VPW, and SCI. This is a much broader diagnostic/transmit instrument. Since our ESP32-S3 supports native USB, the CP2102 is not automatically needed. USB ESD protection remains relevant. Its multiple bus circuits must not be collapsed into a single assumed CCD interface.
- The ChryslerScanner pin table assigns CCD to J1962 pins 3 and 11, PCI/VPW to pin 2, and several SCI lines to other pins; these are ecosystem clues, not verified 1999 Prowler pin assignments. Confirm every DLC connection in vehicle-specific service material before claiming coverage.
- CCDBusTransceiver V1.XX uses +5 V, UART RX/TX, ground, CCD+/- and selectable TBEN bias/termination; its project says disconnect TBEN jumpers for a vehicle network. It is not a direct ESP32-S3 product module and is not included in the P0 BOM.
- The comparator/MOSFET proposal shared in discussion is not adopted as a complete circuit. P0 omits every transmit component and any bus bias/termination. The CMOS comparator input network still requires protection and bus-loading validation.

## Do not order yet

Do not order a final J1962 connector, automotive power front end, TVS, SCI receiver, or PCB until the Prowler DLC pin map, connector geometry, required signal layers, and power budget are verified. The only semiconductor purchase suitable for the current bench-receiver investigation is a small quantity of TLV3212-Q1; a comparator already in the parts bin can be evaluated first if its input range and output behavior fit a safe isolated test.

The P0 device remains receive-only. No CCD transmitter, SCI transmitter, OBD request generation, P1 resistor-key output, or P1 12 V reverse-camera trigger is in this BOM.

