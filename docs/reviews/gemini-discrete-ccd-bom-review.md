# Review: suggested discrete CCD interface BOM

Status: design-review notes; **not** a schematic or build instruction

The supplied Gemini text is treated as a set of claims to verify. It correctly points toward a discrete comparator receiver plus a separately controlled MOSFET transmitter, but multiple electrical details in the proposed BOM are unverified or misleading for the Prowler. No board should be built from that table as written.

## CCD bus claims

- **Prowler documentation:** the 1999 service information says the CCD twisted-pair conductors are each approximately 2.5 V and describes the bus bias/termination network. It does not describe normal bits as CCD+ at 5 V and CCD- at 0 V. A line near 5 V or 0 V should be treated as a fault or measurement condition until the exact OEM diagnostic context is established.
- Community transceiver redesign material describes the *differential* signal as small around that common-mode level (with details varying by circuit and termination). It is not a substitute for measuring the Prowler's bus.
- The claim that the Prowler always has a particular BCM/PCM providing bias and termination is not established for this vehicle configuration. Do not add 10 kΩ/20 kΩ idle bias, termination, or any other bus load to the P0 tap. The proposed bias direction may actively oppose the installed network.
- A 1N4148 in series with each MOSFET drain is not a generic back-power fix. Forward drops and diode paths can change the bus differential voltage and waveform; only include such parts if the complete circuit analysis demonstrates their role.

## Comparator and transmit claims

- **LM393 output:** its output is open-collector, so it needs a pull-up. A pull-up to 3.3 V is appropriate for an ESP32 input if the selected device and surrounding protection support it; never pull the RX pin to 5 V.
- **LM393 input range:** the standard LM393 common-mode range stops about 1.5 V below its positive supply. With a 3.3 V supply, a 2.5 V CCD common-mode input is outside that specified range. A 5 V comparator supply or a comparator with a suitable common-mode range is required. The standard LM393 grade is not an automotive temperature-qualified device; the selected TI TLV3212-Q1 remains the preferred comparator candidate pending circuit validation.
- **Comparator polarity:** wiring CCD+ to (+) and CCD- to (-) makes the comparator output release high when CCD+ is above CCD-. It does not, by itself, establish the expected UART polarity. Determine polarity from actual CCD waveforms and framing tests.
- **MOSFET gate drive:** ESP32 3.3 V GPIO cannot be assumed to switch a P-channel device whose source is on a 5 V rail fully off. The gate driver must define safe states at power-up, reset and MCU loss, and keep VGS within limits. Gate resistors tune switching edges; they do not make a GPIO-to-vehicle interface safe.
- **IRF7317:** historical dual N/P example, but it is end-of-life and the N/P channel RDS(on) specifications are substantially different. “Dual” does not mean matched. The currently active Infineon ISA170230C04LMDS is a bench candidate only; its data does not prove CCD suitability or vehicle-grade qualification.
- **Transmission behavior:** a discrete driver must release the bus for recessive bits, apply the correct current-limited differential dominant state, observe other nodes, and implement CCD arbitration/idle timing. A naive push-pull 5 V/ground drive is not an acceptable interpretation of the CCD physical layer.

## Protection claims

- Nexperia describes PESD1CAN as a CAN protection part and currently marks it **Not for Design In**. Its 24 V reverse standoff and roughly 40 V clamp at 1 A do not by themselves protect a low-voltage comparator input from all vehicle faults. Protection must be coordinated with series impedance, clamp paths, parasitic capacitance, bus loading and the comparator's absolute maximum ratings.
- Do not choose a TVS only because its product name includes CAN. Select protection from the measured CCD signal envelope and defined fault/transient tests. P0 uses a high-impedance, receive-only tap; do not add shunt capacitance or loading without checking its effect.

## MCU and framing

An ESP32-S3 is adequate for raw capture and host-side analysis. The legacy interface documents a typical 7812.5 bit/s bus rate, but a UART byte stream alone does not supply the full CCD framing, bus-idle, collision or arbitration behavior. Implement those semantics only from source-backed protocol research and isolated replay tests.

## Steering/head-unit output claims

- Do not select MCP4131/MCP41010/AD5245 as a default KEY1/KEY2 solution. A digital potentiometer only operates within its terminal-voltage, supply and wiper-current limits; the head unit's KEY bias, resistor ladder, common ground and input impedance are unknown. The named digipots have limited analog-terminal ranges that may not tolerate an unknown head-unit input.
- First measure the head-unit key input voltage, resistance ladder, common reference, current and timing. A better starting architecture for button emulation is fixed, measured resistor values selected by a validated analog switch or relay, with the switch voltage rating and off-state leakage chosen for the measured circuit. A PC817 phototransistor is not a precision resistor; do not assume it creates a stable resistor value.
- A volume-up/down pulse can change the head-unit's relative volume, but it cannot establish the absolute current volume. Manual volume changes made at the head unit may be invisible to a CCD controller. Autovolume state reconciliation therefore remains an explicit P1 design question; do not claim manual-volume preservation until it is demonstrated on the chosen head unit.

## Salvaged legacy ICs

Harvesting a CDP68HC68S1 from an unrelated donor module could provide a lab sample, but it does not resolve counterfeit risk, pinout/board integration work, or future supply. It is not required for the supported discrete architecture, and the unknown Chrysler ASIC markings are not an alternative without verified pinout and limits.

## Disposition

Keep the comparator-plus-MOSFET architecture under evaluation. Reject the proposed 5 V/0 V normal-bit model, added idle-bias resistors, assumed generic TVS/series-diode placement, unmeasured KEY wiring, and claim that volume-step commands alone preserve absolute user volume. The next hardware artifact should be a reviewed schematic and test plan, not a BOM-only prototype. Vehicle transmission remains prohibited until the established review, bench-test and explicit-authorization gates are met.
