# Prioritized backlog

## P0 core: genuine passive CCD capture

1. **Design reference / installation gate:** Use the already archived 1997/1999 Prowler service manual for design and record exact page/figure references. Elvira is a 2000; treat applicability as a carryover assumption. Consult the owner's paper 2000 manual for critical DLC cavities/view, CCD polarity, grounds, fused power and electrical limits as needed for design decisions. Saved 2000 factory diagrams in Drive should be checked first. This does not block schematic development from the archived manual.
2. **Blocker:** Finish positive transient protection, leakage/offset corners and the complete protected power schematic. The connected 25-component CCD subsystem and nominal SPICE results now exist. Specify the remaining input envelope, fault limits, timing and test points. No bus bias/termination; populated bench TX stays jumper-inhibited for vehicle capture.
3. **Blocker:** Select a J1962 male edge connector from full mechanical data; create/measure its footprint and prove enclosure fit. The reference project's `OBD2-90` library footprint name is not a part number.
4. **P0:** Update the KiCad PCB to include the real J1962 edge connector, protected CCD front end, ESP32-S3, USB-C, status/debug points, and protected power. Route using FreeRouting, import the session, review in KiCad, and rerun DRC.
5. **P0:** Validate the receiver and power chain on an isolated bench: waveform levels, polarity, input loading, timestamp fidelity, startup/reset/disconnect and error recovery. Keep the physical TX power jumper absent for P0 vehicle capture.
6. **P0:** Implement ESP32-S3 capture with bounded queues, microsecond monotonic timestamps, raw frames/checksum/error/drop metadata, USB serial export and device version reporting.
7. **P0:** Implement local Wi-Fi AP and a CCD capture/status web view with downloadable raw capture. Keep the capture record schema extensible with thread identity.
8. **P0:** First genuine Prowler CCD capture only after steps 1-7; stationary setup, receive-only, no scan-tool queries.
9. **P0:** Decode and correlate vehicle speed, BCM volume offset, steering events, selector, transmission range (especially Reverse), and lighting using repeated stationary or later offline captures.

## P0 stretch: more DLC lines and full OBD-II behavior

10. Verify which PCI/VPW and SCI lines are populated on this Prowler from OEM documentation/inspection; never infer from another Chrysler model.
11. Add separate protocol-specific receive channels and web tabs for confirmed additional DLC lines. Preserve independent timestamps and loss counters.
12. Decide whether to add a transparent 16-contact pass-through connector for use with a scan tool during logging. Verify continuity and prove that the passive taps do not materially load the bus.
13. Implement reviewed diagnostic request/reply capture on an isolated network first. It is outside P0 core. Any vehicle-side transmission requires electrical/arbitration/failure review, passing bench tests, and explicit owner authorization.

## Platform and future milestones

14. Audit upstream repositories at exact commit hashes, record licenses and protocol assumptions, and resolve project licensing before any code/artwork reuse.
15. Establish isolated virtual CCD network and replay harness, then review OEM radio periodic/request-response behavior and module emulation.
16. Research CCD TPMS module/sensor emulation for newer sensors; establish message set, enrollment behavior, timing and compatibility on an isolated network.
17. **P1 blocker:** Measure Android head-unit KEY1/KEY2 and reverse-trigger input voltage, impedance, resistor ladder, timing, current and ground assumptions.
18. **P1:** Map validated BCM autovolume offset changes to bounded relative volume-up/down pulses; preserve manual steering volume, handle resets/data loss, and prevent command storms. Do not estimate absolute head-unit volume.
19. **P1:** Design a serviceable behind-radio adapter harness and electrically safe resistor-command output stage after head-unit measurements.
20. **P1:** Decode transmission range and drive the Android unit's reverse-camera input with a protected, default-low 12 V output. Never drive OEM reverse-lamp wiring.
21. Add CI, static analysis, SPDX/project licensing, hardware review, safety procedures and release checks.
