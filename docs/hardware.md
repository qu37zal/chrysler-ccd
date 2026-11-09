# Preliminary hardware interface and BOM

No final PCB artwork until bus loading, transceiver compatibility and exact connector details are verified.

| Function | Candidate | Status |
|---|---|---|
| MCU | ESP32-S3 module/devkit | Selected platform |
| CCD physical interface | Receiver path from qualified CDP68HC68S1-family CCD transceiver or documented CCDBusTransceiver design | Candidate only; verify supply, clock, levels, datasheet and availability |
| Bus protection | Series impedance and low-capacitance automotive-rated protection selected from transceiver limits | Not selected; needs measured bus envelope and load budget |
| OBD | Reversible breakout to DLC 3/11, 4/5 ground, 16 protected supply | Pin map cross-check required; no connection yet |
| Power | Automotive input protection, reverse polarity, surge suppression, buck to 5V/3V3 | Design pending crank/transient requirements |
| Debug | USB-C, status LEDs, test points for bus+/-, receiver output, 3V3 and ground | Preliminary |

Power-up must default to receiver-only; omit TX path and bus bias/termination. Isolate MCU ground and vehicle ground only per verified design. Validate bus input loading on a bench before vehicle connection.
