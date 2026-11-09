# Candidate signal dictionary

Confidence: **A** direct 1999 Prowler service documentation; **B** corroborated platform reference, needs Prowler confirmation; **U** unknown.

| Signal | Candidate source/value | Confidence | Evidence / next validation |
|---|---|---|---|
| CCD physical pair | Twisted pair, nominal ~2.5 V each with divider network | A | 1999 service information; confirm exact test page/circuit before interface |
| DLC CCD pins | 3 (+), 11 (-) | B | Chrysler diagnostic documentation; validate against Prowler DLC drawing |
| Steering switch resistor codes | Unknown | U | Prowler wiring diagram and stationary switch-state captures |
| Steering command frame IDs/data | Unknown; 0x24/0xE4 unverified leads | U | Controlled repeated captures; no assumptions |
| Vehicle speed encoding | Unknown | U | Compare stationary and controlled documented speed references |
| OFF/LOW/HIGH selector | Known factory settings, electrical/message encoding unknown | U | Service wiring/troubleshooting and switch measurements |
| OEM radio diagnostics/periodic traffic | Unknown | U | Factory radio manual and isolated capture/bench study |
