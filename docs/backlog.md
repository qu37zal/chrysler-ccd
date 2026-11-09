# Prioritized backlog

1. **P0 blocker:** Obtain Prowler 1999 OEM wiring/service pages for DLC, radio connector, BCM and speed-sensitive selector; capture page references and license/access terms.
2. **P0 blocker:** Audit upstream repositories at exact commit hashes; record licenses, protocol assumptions and reusable algorithms. Resolve project license before reuse.
3. **P0 blocker:** Select a documented CCD receiver and design a powered-off-safe, bus-loading-bounded interface; verify no transmit/bias/termination path.
4. **P0:** Implement hardware UART/RMT receive framing with microsecond timestamp and overflow accounting; capture raw bytes and checksum status.
5. **P0:** Validate interface against isolated CCD signal source and logic analyzer, including reversed polarity, malformed data, disconnect and MCU reset.
6. **P0:** Expand host replay fixtures and frame parser using independently sourced checksum/framing specification.
7. **P0:** Implement stationary event annotation and deterministic capture correlation report; preserve full provenance.
8. **P0:** First genuine Prowler capture only after steps 1–5; use passive receiver at DLC pins 3/11, stationary vehicle, no scan-tool transmission.
9. **P0:** Verify vehicle speed, steering controls, selector and lighting/reverse associations with repeated controlled stationary or safe offline captures.
10. **Bench emulation:** Establish isolated virtual CCD bus and OEM radio request/response/periodic behavior; review before any transmitter implementation.
11. **P1 blocker:** Measure Android head unit KEY1/KEY2 input impedance, reference voltage, common ground and resistor ladder with its documentation and isolated bench setup.
12. **P1:** Implement autovolume deterministic simulation with manual changes, no-volume-state recovery, reset, loss, hysteresis, bounded increments and all three modes.
13. **P1:** Design serviceable behind-radio adapter harness and output hardware after electrical assumptions are measured.
14. **Release:** Add CI, static analysis, SPDX/project licensing, hardware review and safety checklist.
