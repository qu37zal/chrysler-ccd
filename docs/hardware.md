# Hardware design status

Current choices: [P0 BOM](p0-bom.md). The connected [CCD subsystem](../hardware/kicad/p0_frontend/README.md)
has 25 components, [bench purchase CSVs](../hardware/bom/README.md), and
[synthetic SPICE fixtures/results](../simulation/README.md).

The old p0_carrier is superseded. No complete PCB is released for fabrication.
CCD protection, the power path, OBD footprint, USB/MCU integration and physical
validation remain required before release.

P0 packages OBD and USB on opposite enclosure ends, with ESP32-S3 Wi-Fi AP/web
access. The enclosure must carry insertion loads without loading solder joints,
retain the PCB, preserve antenna clearance and allow reset/boot and jumper
inspection. The populated bench transmitter is authorized; keep its jumper absent
for vehicle capture. Vehicle transmission is unauthorized.

Intersil CDP68HC68S1 is obsolete. The reported Philips/Signetics 4632650 Chrysler
ASIC has no verified public pinout and is not a documented pin-compatible
substitute. Neither it nor IRF7317 is selected. LT1716 at 3.3 V supersedes earlier
TLV3212-Q1/TLV1701 receiver candidates because its inputs can exceed its supply.
Its model supports nominal exploration; leakage, protection, timing and faults
still need physical checks.

The [Gemini BOM review](reviews/gemini-discrete-ccd-bom-review.md) records earlier
hypotheses/corrections and is not the current circuit. Preserve source-year
distinctions, add no unverified bus bias/termination, and keep other protocols
separate from CCD.
