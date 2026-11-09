# Preliminary hardware interface and BOM

No final PCB artwork until bus loading, transceiver compatibility and exact connector details are verified.

Review of the supplied comparator/MOSFET/KEY-input BOM notes is recorded in [Gemini discrete CCD BOM review](reviews/gemini-discrete-ccd-bom-review.md). Those notes are a hypothesis list, not a build-ready design.

The itemized prototype parts and explicit unselected items are tracked in the [P0 preliminary BOM](p0-bom.md).

| Function | Candidate | Status |
|---|---|---|
| MCU | ESP32-S3 module/devkit | Selected platform |
| CCD interface legacy IC | Intersil CDP68HC68S1E, DIP-14 | Documented legacy serial bus interface IC. Obsolete/out of production, 4–7 V supply, not 3.3 V logic. Not the default P0 choice. |
| Candidate supported receive IC | TI TLV3212-Q1 dual comparator | ACTIVE, current automotive-qualified comparator family; 1.8–5.5 V supply and rail-to-rail input range. Candidate for a discrete CCD receiver. Not a CCD transceiver. |
| Future transmit section | Infineon ISA170230C04LMDSXTMA1 dual N/P MOSFET, evaluation candidate | Active/preferred SO-8 dual N/P, 40 V, logic-level; specified maximum RDS(on) at 4.5 V is 29.5 mΩ N-channel and 23.6 mΩ P-channel. More balanced than IRF7317, but not a matched pair and not yet approved for this topology. Keep TX unpopulated and disconnected during P0 vehicle capture. |
| CCD interface development board | Chrysler Scanner CCDBusTransceiver V1.03, part BC-002103 | Candidate receiver/transmitter board; datasheet specifies 5 V UART and selectable bus bias/termination. Not ESP32-ready without level adaptation and confirmed TX disable; current sales availability unverified. |
| P0 receiver-only front end | High-impedance differential comparator/receiver with input protection and 3.3 V output | Preferred direction pending schematic review and bench validation. Do not populate transmitter, bias, or termination for initial vehicle capture. |
| Bus protection | Series impedance and low-capacitance automotive-rated protection selected from transceiver limits | Not selected; needs measured bus envelope and load budget |
| OBD | J1962 male plug; CCD candidate at DLC 3/11; grounds 4/5; protected supply 16; survey all populated signal pins | Plug-in P0 dongle concept; Prowler-specific pin map required before wiring |
| OBD enclosure connector | J1962 male plug at vehicle end | Full 16-contact connector; only verified diagnostic lines receive high-impedance protected taps |
| Power | Automotive input protection, reverse polarity, surge suppression, buck to 5V/3V3 | Design pending crank/transient requirements |
| P1 reverse-camera trigger | Protected automotive high-side switch, e.g. TI TPS1H200A-Q1 | Study candidate only. ACTIVE, AEC-Q100, 3.4–40 V supply, protected switch. Confirm Android trigger input voltage/current and fault behavior before choosing current limit, series protection or schematic. Output defaults low. Not part of receive-only P0. |
| Debug | USB-C, status LEDs, test points for bus+/-, receiver output, 3V3 and ground | Preliminary |

Power-up must default to receiver-only; omit TX path and bus bias/termination. Isolate MCU ground and vehicle ground only per verified design. Validate bus input loading on a bench before vehicle connection. The enclosure uses a J1962 male vehicle plug and USB-C at the opposite end. The 16 contacts are present, but only confirmed lines are monitored; no female pass-through connector is included in this packaging concept.

## Network and interaction scope

Initial P0 uses the ESP32-S3 as a local 2.4 GHz Wi-Fi access point with a browser GUI for device status, configuration, live traffic and capture export. Protect the AP with a configurable password; no internet/cloud service is needed. Bluetooth and a native iOS app are deferred. “Sniff all data” means passively record every decodable transmission on each populated, vehicle-accessible diagnostic line at the DLC. CCD is a two-wire differential bus at pins 3/11; Chrysler diagnostic tools also support SCI through separate DLC pins on some applications, so P0 must inventory the Prowler's actual populated signal pins and their transceivers before declaring coverage. Passive receive cannot reveal query/response data that is not transmitted until a scan tool asks for it. Do not actively query in the first milestone.

P0 captures are expected to support P1 discovery of BCM volume-offset levels, vehicle speed, steering events and transmission range. P0 itself remains receive-only and does not connect to the Android head unit. P1 uses an adapter harness behind the head unit. The reverse-camera request is a separate P1 output: raise the Android unit's measured reverse-trigger input to a protected 12 V source only while a fresh, validated CCD transmission-range signal says Reverse. Use a protected automotive high-side stage with default-off behavior in hardware; go low immediately on stale/invalid data, reset or power loss. Do not connect this output to the OEM reverse lamps. Verify the Android unit's trigger voltage/current and reference before designing the output circuit.

## Enclosure requirements

Design for a compact, serviceable 3D-printed dongle with a J1962 male plug at the vehicle end and USB-C at the opposite end. A female scan-tool pass-through is not included in this packaging concept. Route only confirmed diagnostic lines to high-impedance, independently protected receive front ends; do not assume the other J1962 contacts are covered. Include visible status indication, reset/recovery access, secure fasteners, and internal retention for the ESP32 and interface board. Do not finalize CAD until connector dimensions, USB clearances, power protection, and board stack are measured.

## Ordering recommendation

The documented legacy serial-bus IC is **Intersil CDP68HC68S1E**, 14-pin PDIP (through-hole) or **CDP68HC68S1M**, 20-pin SOIC. It performs differential CCD receive/transmit and has bus arbitration/collision/idle features; the datasheet describes 7812.5 bit/s as the typical bus rate. It handles CCD only, not separate SCI lines, and is obsolete.

The CDP68HC68S1 operates from 4–7 V and uses 5 V logic. It needs a clock source; the datasheet uses a 1 MHz clock example for the common 7812.5 bit/s bus rate. A direct connection to ESP32-S3 GPIO is not safe. Its transmit path must be physically isolated for P0.

### Supported receiver candidate: TI TLV3212-Q1

The Philips/Signetics marking **4632650**, often **4632650-1**, is reported to be a proprietary Chrysler CCD controller/transceiver ASIC in SOP-20 module applications. This matches community observations of the marking on Chrysler modules, but no public manufacturer datasheet or verified pinout has been located. The CDP68HC68S1 datasheet is a useful functional reference for CCD electrical behavior; it is not evidence that 4632650 has the same pinout, timing limits, support network, or drop-in compatibility. Treat those ASIC details as user/community-reported until confirmed from OEM module schematics or measurements. It is not the part to order for our P0 receiver-only prototype.

For the supported-component path, TI **TLV3212-Q1** is a leading candidate for the discrete receiver: a dual comparator (VSSOP-8 or SOIC-8 options) listed ACTIVE by TI, AEC-Q100 qualified, with 1.8–5.5 V supply and input range extending 200 mV beyond either rail. The new family is explicitly positioned as the successor to TLV3202-Q1. It is not a CCD transceiver or drop-in replacement: it does not provide arbitration, idle/CTRL outputs, or a transmitter. A comparator channel can resolve CCD differential polarity as described in the community redesign notes; the external network still needs an engineered input protection and reference circuit.

P0 firmware and hardware should leave a path to later isolated-bench module emulation. The working architecture to investigate is the community-described split transceiver: a comparator for differential RX, plus a complementary N/P MOSFET differential driver for TX, with the microcontroller handling UART timing, CCD framing, arbitration and bus-idle behavior. This is a circuit concept, not an approved schematic. Keep RX and TX as separate circuits: reserve a discrete TX section, but leave its components unpopulated and the physical bus path open for vehicle sniffing. Add a hardware transmit inhibit asserted by default that cannot be cleared by firmware alone during P0. Do not add bus bias or termination.

The **IRF7317** is a historical example of a dual N/P MOSFET used in this concept, but Infineon lists it end-of-life. Its datasheet specifies different maximum RDS(on) values for the N and P channels (29 mΩ and 58 mΩ at 4.5 V), so “dual” does not mean electrically matched. Do not select it as the production part. A current candidate for initial driver bench work is Infineon **ISA170230C04LMDSXTMA1** (SO-8): active/preferred, 40 V, logic-level, and specified at 29.5 mΩ N-channel / 23.6 mΩ P-channel maximum RDS(on) at 4.5 V. This is a better-balanced dual package, but still not a matched pair; its datasheet does not establish suitability for the CCD circuit or automotive qualification. Confirm stock and package details before ordering. Evaluate it against two separate MOSFETs by gate drive, body-diode paths, off-state leakage and measured differential bus swing. TX gate drive, current limiting, arbitration sensing, power-up/reset states and fault containment remain open design work.

The community receiver sketch includes input protection and a comparator converting bus differential polarity to a single-ended UART RX signal. For this ESP32-S3 design, the comparator output must be pulled or level-shifted to 3.3 V; do not copy a 5 V pull-up directly to an ESP32 GPIO. Verify receiver threshold and hysteresis against real CCD idle and dominant/recessive amplitudes, then test bus loading and protection on an isolated source.

**Order suggestion:** one or two TLV3212-Q1 devices in a hobbyist-assemblable package, preferably SOIC-8 (`TLV3212QDRQ1`) if available from an authorized distributor; VSSOP-8 orderable is `TLV3212QDGKRQ1`. This covers candidate receive-channel prototyping only. TX components should wait until the discrete driver schematic and protection/arbitration analysis are reviewed. Check live stock before ordering: at research time TI listed the family ACTIVE, while DigiKey showed the VSSOP automotive orderable out of stock with a long lead time. If the Q1 part cannot be sourced promptly, tell me what comparator parts are already in your bin and we can check whether one supports a safe bench prototype. Avoid counterfeit-marketplace legacy SBICs as the basis for the P0 design.

TLV3212-Q1 is a candidate IC, not a finished electrical design. Its input absolute maximum limits do not tolerate arbitrary automotive transients; series impedance and external protection are still mandatory. We have not validated a circuit against the Prowler bus or measured tap loading. Do not connect a prototype to the vehicle before the front end passes isolated-bench checks.

The CCDBusTransceiver V1.03 board (BC-002103) is a useful bench reference, not a drop-in P0 part: its datasheet specifies 5 V UART and has selectable termination/bias jumpers. If one is purchased for bench characterization, keep its transmitter disconnected and remove TBEN jumpers for live-bus use; still level-shift its RX output before an ESP32. Availability must be checked with the seller.
