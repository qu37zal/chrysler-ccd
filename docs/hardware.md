# Preliminary hardware interface and BOM

No final PCB artwork until bus loading, transceiver compatibility and exact connector details are verified.

| Function | Candidate | Status |
|---|---|---|
| MCU | ESP32-S3 module/devkit | Selected platform |
| CCD interface legacy IC | Intersil CDP68HC68S1E, DIP-14 | Documented legacy serial bus interface IC. Obsolete/out of production, 4–7 V supply, not 3.3 V logic. Not the default P0 choice. |
| Candidate supported receiver IC | TI TLV3212-Q1 dual comparator | ACTIVE, current automotive-qualified comparator family; 1.8–5.5 V supply and rail-to-rail input range. A discrete receive-only comparator front end can use one channel. Not a drop-in CCD transceiver: no arbitration, bus-idle, transmit or CCD-specific functions. Bench design/validation still required. |
| CCD interface development board | Chrysler Scanner CCDBusTransceiver V1.03, part BC-002103 | Candidate receiver/transmitter board; datasheet specifies 5 V UART and selectable bus bias/termination. Not ESP32-ready without level adaptation and confirmed TX disable; current sales availability unverified. |
| P0 receiver-only front end | High-impedance differential comparator/receiver with input protection and 3.3 V output | Preferred direction pending schematic review and bench validation. Do not populate transmitter, bias, or termination for initial vehicle capture. |
| Bus protection | Series impedance and low-capacitance automotive-rated protection selected from transceiver limits | Not selected; needs measured bus envelope and load budget |
| OBD | Reversible breakout; CCD candidate at DLC 3/11; grounds 4/5; protected supply 16; survey all populated signal pins | Prowler-specific pin map required; no connection yet |
| OBD enclosure connector | Automotive 16-pin J1962 male plug with fully wired 16-pin female pass-through | Preserve straight-through continuity for all pins and add only high-impedance monitoring taps. Verify there are no shorts, cross-connects, or monitor loading on unrelated pins. |
| Power | Automotive input protection, reverse polarity, surge suppression, buck to 5V/3V3 | Design pending crank/transient requirements |
| Debug | USB-C, status LEDs, test points for bus+/-, receiver output, 3V3 and ground | Preliminary |

Power-up must default to receiver-only; omit TX path and bus bias/termination. Isolate MCU ground and vehicle ground only per verified design. Validate bus input loading on a bench before vehicle connection. The enclosure should expose a fully wired/pass-through OBD-II connection while the sniffer monitors CCD at DLC pins 3 and 11. Establish exact connector/passthrough semantics and all-pin behavior before mechanical design.

## Network and interaction scope

Initial P0 uses the ESP32-S3 as a local 2.4 GHz Wi-Fi access point with a browser GUI for device status, configuration, live traffic and capture export. Protect the AP with a configurable password; no internet/cloud service is needed. Bluetooth and a native iOS app are deferred. “Sniff all data” means passively record every decodable transmission on each populated, vehicle-accessible diagnostic line at the DLC. CCD is a two-wire differential bus at pins 3/11; Chrysler diagnostic tools also support SCI through separate DLC pins on some applications, so P0 must inventory the Prowler's actual populated signal pins and their transceivers before declaring coverage. Passive receive cannot reveal query/response data that is not transmitted until a scan tool asks for it. Do not actively query in the first milestone.

## Enclosure requirements

Design for a compact, strain-relieved 3D printed housing with an automotive-grade J1962 male plug to the vehicle and a fully wired 16-pin J1962 female pass-through socket for a scan tool. Preserve all 16 pin-to-pin connections. Route each monitored channel as a high-impedance tap with independent protection and no driver path. Include access to USB, visible status indication, reset/recovery access, secure fasteners, and an internal retention feature for the ESP32 and interface board. Do not finalize CAD until connector dimensions, cable exit/bend radius, fuse/protection components, and board stack are measured.

## Ordering recommendation

The documented legacy serial-bus IC is **Intersil CDP68HC68S1E**, 14-pin PDIP (through-hole) or **CDP68HC68S1M**, 20-pin SOIC. It performs differential CCD receive/transmit and has bus arbitration/collision/idle features; the datasheet describes 7812.5 bit/s as the typical bus rate. It handles CCD only, not separate SCI lines, and is obsolete.

The CDP68HC68S1 operates from 4–7 V and uses 5 V logic. It needs a clock source; the datasheet uses a 1 MHz clock example for the common 7812.5 bit/s bus rate. A direct connection to ESP32-S3 GPIO is not safe. Its transmit path must be physically isolated for P0.

### Supported receiver candidate: TI TLV3212-Q1

The Philips/Signetics marking **4632650**, often **4632650-1**, is reported to be a proprietary Chrysler CCD controller/transceiver ASIC in SOP-20 module applications. This matches community observations of the marking on Chrysler modules, but no public manufacturer datasheet or verified pinout has been located. The CDP68HC68S1 datasheet is a useful functional reference for CCD electrical behavior; it is not evidence that 4632650 has the same pinout, timing limits, support network, or drop-in compatibility. Treat those ASIC details as user/community-reported until confirmed from OEM module schematics or measurements. It is not the part to order for our P0 receiver-only prototype.

For a currently supported **receive-only** P0 front end, the leading candidate is TI **TLV3212-Q1**, a dual comparator (VSSOP-8 or SOIC-8 options) listed ACTIVE by TI, AEC-Q100 qualified, with 1.8–5.5 V supply and input range extending 200 mV beyond either rail. The new family is explicitly positioned as the successor to TLV3202-Q1. It is not a CCD transceiver or drop-in replacement: it does not provide arbitration, idle/CTRL outputs, or a transmitter. A single comparator channel can resolve CCD differential polarity as described in the community redesign notes; the external network still needs an engineered input protection and reference circuit. No bus bias, termination or transmitter should be fitted for P0.

**Order suggestion:** one or two TLV3212-Q1 devices in a hobbyist-assemblable package, preferably SOIC-8 (`TLV3212QDRQ1`) if available from an authorized distributor; VSSOP-8 orderable is `TLV3212QDGKRQ1`. Check live stock before ordering: at research time TI listed the family ACTIVE, while DigiKey showed the VSSOP automotive orderable out of stock with a long lead time. If the Q1 part cannot be sourced promptly, tell me what comparator parts are already in your bin and we can check whether one supports a safe bench prototype. Avoid counterfeit-marketplace legacy SBICs as the basis for the P0 design.

TLV3212-Q1 is a candidate IC, not a finished electrical design. Its input absolute maximum limits do not tolerate arbitrary automotive transients; series impedance and external protection are still mandatory. We have not validated a circuit against the Prowler bus or measured tap loading. Do not connect a prototype to the vehicle before the front end passes isolated-bench checks.

The CCDBusTransceiver V1.03 board (BC-002103) is a useful bench reference, not a drop-in P0 part: its datasheet specifies 5 V UART and has selectable termination/bias jumpers. If one is purchased for bench characterization, keep its transmitter disconnected and remove TBEN jumpers for live-bus use; still level-shift its RX output before an ESP32. Availability must be checked with the seller.
