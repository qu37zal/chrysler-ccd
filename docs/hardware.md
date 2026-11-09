# Preliminary hardware interface and BOM

No final PCB artwork until bus loading, transceiver compatibility and exact connector details are verified.

| Function | Candidate | Status |
|---|---|---|
| MCU | ESP32-S3 module/devkit | Selected platform |
| CCD interface legacy IC | Intersil CDP68HC68S1E, DIP-14 | Identified legacy serial bus interface IC. Obsolete/out of production, 4–7 V supply, not 3.3 V logic. Do not order for P0 without confirming authenticity, package, support circuitry, and receive-only isolation. |
| CCD interface development board | Chrysler Scanner CCDBusTransceiver V1.03, part BC-002103 | Candidate receiver/transmitter board; datasheet specifies 5 V UART and selectable bus bias/termination. Not ESP32-ready without level adaptation and confirmed TX disable; current sales availability unverified. |
| P0 receiver-only front end | High-impedance differential comparator/receiver with input protection and 3.3 V output | Preferred direction pending schematic review and bench validation. Do not populate transmitter, bias, or termination for initial vehicle capture. |
| Bus protection | Series impedance and low-capacitance automotive-rated protection selected from transceiver limits | Not selected; needs measured bus envelope and load budget |
| OBD | Reversible breakout to DLC 3/11, 4/5 ground, 16 protected supply | Pin map cross-check required; no connection yet |
| OBD enclosure connector | Automotive 16-pin J1962 pass-through arrangement | Decide between male plug with female pass-through and a short harness; preserve pin continuity only where required and ensure no unwanted module loading |
| Power | Automotive input protection, reverse polarity, surge suppression, buck to 5V/3V3 | Design pending crank/transient requirements |
| Debug | USB-C, status LEDs, test points for bus+/-, receiver output, 3V3 and ground | Preliminary |

Power-up must default to receiver-only; omit TX path and bus bias/termination. Isolate MCU ground and vehicle ground only per verified design. Validate bus input loading on a bench before vehicle connection. The enclosure should expose a fully wired/pass-through OBD-II connection while the sniffer monitors CCD at DLC pins 3 and 11. Establish exact connector/passthrough semantics and all-pin behavior before mechanical design.

## Network and interaction scope

Initial P0 uses the ESP32-S3 as a local 2.4 GHz Wi-Fi access point with a browser GUI for device status, configuration, live traffic and capture export. Protect the AP with a configurable password; no internet/cloud service is needed. Bluetooth and a native iOS app are deferred. “Sniff all data” means receive every decodable transmission physically present on the CCD pair available at the OBD-II connector; it does not promise visibility into non-CCD links, isolated module links, or messages not routed to the DLC. Any additional DLC pins are initially monitored only if their physical interface is independently identified and safely validated.

## Enclosure requirements

Design for a compact, strain-relieved 3D printed housing with an automotive-grade J1962 male plug to the vehicle and a fully wired J1962 female pass-through socket for a scan tool. Preserve only the pass-through pin connections required by the vehicle/scan-tool interface; route the CCD receiver as a high-impedance tap. The exact “fully implemented” pin list is an open decision pending a pin-continuity plan. Include access to USB, visible status indication, reset/recovery access, secure fasteners, and an internal retention feature for the ESP32 and interface board. Do not finalize CAD until connector dimensions, cable exit/bend radius, fuse/protection components, and board stack are measured.

## Ordering recommendation

The legacy serial-bus IC is **Intersil CDP68HC68S1E**, 14-pin PDIP (through-hole) or **CDP68HC68S1M**, 20-pin SOIC. That is the part you are thinking of. It performs differential CCD receive/transmit and has bus arbitration/collision/idle features; the datasheet describes 7812.5 bit/s as the typical bus rate. The “E” suffix is the easiest hobbyist package, but this is an obsolete part and broker/marketplace stock is not assured genuine.

The CDP68HC68S1 operates from 4–7 V and uses 5 V logic. It also needs a clock source; the datasheet uses a 1 MHz clock example for the common 7812.5 bit/s bus rate. Its bus pins need correctly designed external bias/termination support in a network, and its transmit section is active. A direct connection to ESP32-S3 GPIO is not safe: use proper 3.3 V level adaptation on receive and keep the bus transmit path physically absent or disabled for P0. If you order one, buy a single DIP-14 sample from a source you trust for isolated-bench characterization only; don’t connect it to the vehicle yet. A receiver-only comparator path remains the safer P0 architecture, and may use parts already in your bin.

The CCDBusTransceiver V1.03 board (BC-002103) is a useful bench reference, not a drop-in P0 part: its datasheet specifies 5 V UART and has selectable termination/bias jumpers. If one is purchased for bench characterization, keep its transmitter disconnected and remove TBEN jumpers for live-bus use; still level-shift its RX output before an ESP32. Availability must be checked with the seller.
