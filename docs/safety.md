# Safety and validation

1. Review the exact transceiver datasheet; check bus absolute maximums and receiver load. Use isolated/current-limited bench supply first.
2. Validate logic output, polarity, timing and powered-off leakage using a function generator or isolated CCD bench source. No vehicle connection at this stage.
3. Verify PCB/harness has no path from MCU TX to bus; omit bus bias/termination. Measure resistance and powered-off leakage before use.
4. Test firmware with synthetic byte streams, overflow injection, reset and disconnect. Confirm loss counters and safe startup.
5. With ignition off and a verified protected high-impedance receiver only, connect through an OBD breakout; inspect stationary. Disconnect on any module warning or abnormal bus voltage.
6. Record ignition state and stationary control changes; operate vehicle only after parking. Driver must never use logging/diagnostic software while driving.
7. Vehicle transmission remains prohibited until circuit, arbitration, behavior and bench evidence are reviewed and the user explicitly authorizes it.
