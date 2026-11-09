# Prioritized backlog

1. **P0 blocker:** Obtain Prowler 1999 OEM wiring/service pages for every DLC cavity, radio connector, BCM and speed-sensitive selector; determine whether separate SCI/other diagnostic signals are populated and record each layer/pin. Capture page references and license/access terms.
2. **P0 blocker:** Inspect parts-bin inventory and select a 3.3 V receive-only CCD front end with verified input protection and loading. Decide between a comparator circuit and documented transceiver board after checking component availability; do not order obsolete CDP68HC68S1E as the default.
3. **P0 blocker:** Audit upstream repositories at exact commit hashes; record licenses, protocol assumptions and reusable algorithms. Resolve project license before reuse.
4. **P0 blocker:** Design protected automotive power and a modular CCD front end: comparator RX plus reserved, unpopulated complementary N/P MOSFET differential TX stage for later bench emulation. Keep TX physically disconnected and hardware-inhibited by default; no bus bias or termination. Select modern MOSFETs after swing/current-balance analysis; IRF7317 is end-of-life and its N/P channels are not closely matched. Define isolated-bench TX validation and arbitration/fault review as later gates.
5. **P0:** Implement hardware UART/RMT receive framing with microsecond timestamp and overflow accounting; capture raw bytes and checksum status.
6. **P0:** Validate interface against isolated CCD signal source and logic analyzer, including reversed polarity, malformed data, disconnect and MCU reset.
7. **P0:** Expand host replay fixtures and frame parser using independently sourced checksum/framing specification.
8. **P0:** Implement local Wi-Fi AP, authenticated/configurable browser interface, live counters and downloadable capture format; no cloud dependency.
9. **P0:** Mechanically define enclosure and OBD J1962 male/female pass-through semantics, pin continuity and strain relief before CAD/printing.
10. **P0:** Implement stationary event annotation and deterministic capture correlation report; preserve full provenance.
11. **P0:** First genuine Prowler capture only after steps 1–6; use passive receiver(s) on verified DLC pins, stationary vehicle, no scan-tool transmission.
12. **P0:** Verify vehicle speed, steering controls, autovolume offset, selector, transmission range (especially Reverse), and lighting associations with repeated controlled stationary or safe offline captures. P0 collects signals passively for later P1 use.
13. **Later:** Bluetooth and native iOS app, after P0 capture integrity and local web UX are established.
14. **Bench emulation:** Establish isolated virtual CCD bus and OEM radio request/response/periodic behavior; review before any transmitter implementation.
15. **P1 blocker:** Measure Android head unit KEY1/KEY2 and reverse-trigger input impedance, reference voltage, thresholds, current and common ground with its documentation and isolated bench setup.
16. **P1:** Decode the BCM's relative autovolume offset and selector behavior; then use the deterministic host model to map BCM offset changes to bounded volume-up/down pulses. Manual steering volume remains independent, and the user may trim if a pulse is lost. Test data loss, reset/re-baseline, OFF/LOW/HIGH, repeated transitions and pulse-rate limits. Do not infer absolute head-unit volume.
17. **P1:** Design serviceable behind-radio adapter harness and output hardware after electrical assumptions are measured.
18. **Release:** Add CI, static analysis, SPDX/project licensing, hardware review and safety checklist.
19. **Future bench emulation:** Research whether a CCD TPMS module or sensor emulator can support newer tire-pressure sensors; identify required module role, message set, enrollment behavior, timing and compatibility. Keep all prototype transmission isolated from the vehicle.
20. **P1:** Design a protected, default-low 12 V high-side output to the Android head unit's reverse-camera trigger from a verified fresh CCD Reverse state. Confirm the signal decoder and output stage on a bench harness; never use the P1 output to drive OEM reverse-lamp wiring.
