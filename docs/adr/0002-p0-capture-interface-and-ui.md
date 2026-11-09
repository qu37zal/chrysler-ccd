# ADR 0002: P0 capture interface and local UI

Status: Proposed

P0 targets the traffic physically observable on the CCD differential pair at the vehicle's OBD-II DLC. It uses an ESP32-S3, protected receiver-only input, a local Wi-Fi access point and a browser GUI for status, annotations and export. Bluetooth and native iOS support are deferred. The enclosure is planned around a J1962 vehicle connection and scan-tool pass-through; exact pass-through pin continuity remains to be measured and specified.

The CDP68HC68S1E (PDIP-14) is the legacy CCD Serial Bus Interface Chip that simplifies differential bus interfacing. It is obsolete and 5 V; the board has a transmitter. It may be sampled for bench work but is not the default P0 interface. Prefer a high-impedance receiver-only design or isolate/level-shift a validated receiver output, with bus bias/termination omitted.
