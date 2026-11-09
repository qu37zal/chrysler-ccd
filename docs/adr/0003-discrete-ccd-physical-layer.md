# ADR 0003: Discrete CCD physical-layer direction

Status: Proposed for bench evaluation

## Decision under evaluation

Use a split, discrete physical layer rather than designing around the undocumented Philips/Signetics 4632650 ASIC or the obsolete CDP68HC68S1. The receive section will use a protected differential comparator with a 3.3 V MCU-level output. A separate complementary MOSFET driver section may be populated for isolated-bench module emulation after its topology and control behavior are validated.

The first MOSFET device to evaluate is Infineon ISA170230C04LMDSXTMA1, a currently active/preferred 40 V dual N/P SO-8 with specified maximum on-resistance of 29.5 mΩ (N) and 23.6 mΩ (P) at 4.5 V gate drive. It is a candidate, not an approved or matched pair. The comparator candidate is TI TLV3212-Q1.

## Rationale

- This direction uses documented, current-production building blocks and supports future radio, TPMS and other module-emulation experiments.
- RX and TX can be kept electrically separate, enabling a physically transmit-inhibited receive-only P0 device.
- The MCU/software layer can implement CCD framing, message timing, arbitration and idle detection rather than depending on legacy SBIC features.
- The IRF7317 is end-of-life, and its N/P channels have substantially different specified on-resistance values.

## Constraints and validation gates

- No bus bias or termination is to be added without vehicle-specific evidence.
- Do not populate or connect the transmitter during P0 vehicle capture.
- Validate the receiver threshold, common-mode range, protection and bus loading with an isolated source and oscilloscope/logic analyzer.
- Validate TX dominant/recessive differential amplitude, current limiting, MOSFET gate stress, arbitration observation, timeout, reset and stuck-on behavior on an isolated virtual bus.
- The 40 V dual MOSFET is not assumed to be automotive qualified or suitable for the CCD line from its datasheet alone.
- Select the production MOSFET topology only after measured bus behavior and fault analysis. Confirm the 3.3 V/5 V gate-drive strategy; do not drive MOSFET gates directly from ESP32 pins without the reviewed circuit.
- No actual-vehicle transmission without electrical review, passing bench tests and explicit user authorization.

## Sources

- [Chrysler Scanner discrete transceiver redesign notes](https://chryslerccdsci.wordpress.com/2020/03/22/re-designing-the-ccd-bus-transceiver-chip/)
- [Infineon ISA170230C04LMDS product page](https://www.infineon.com/part/ISA170230C04LMDS)
- [TI TLV3212-Q1 product page](https://www.ti.com/product/TLV3212-Q1)
