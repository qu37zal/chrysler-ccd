# Candidate signal dictionary

Confidence: **A** checked against 2000 Prowler factory documentation; **C** documented in the 1999 manual and provisionally carried over to Elvira (2000); **B** corroborated platform reference, needs Prowler confirmation; **R** owner-reported/expected behavior, frame details unverified; **U** unknown.

| Signal | Candidate source/value | Confidence | Evidence / next validation |
|---|---|---|---|
| CCD physical pair | Twisted pair, nominal ~2.5 V each with divider network | C | 1999 service information carried over to 2000; confirm exact test page/circuit before interface |
| DLC CCD pins | 3 (+), 11 (-) | B | Chrysler diagnostic documentation; validate against Prowler DLC drawing |
| Steering switch resistor codes | Unknown | U | Prowler wiring diagram and stationary switch-state captures |
| Steering command frame IDs/data | Unknown; 0x24/0xE4 unverified leads | U | Controlled repeated captures; no assumptions |
| Vehicle speed encoding | Unknown | U | Compare stationary and controlled documented speed references |
| BCM autovolume compensation offset | Owner expects discrete/relative compensation levels to be available over CCD in addition to speed; ID, payload encoding, scale, direction, update rate and selector interaction unknown | R | Capture with OEM radio connected; compare OFF/LOW/HIGH and controlled speed conditions. Confirm whether BCM sends the requested offset and whether the radio applies it directly. |
| Transmission range / reverse state | Unknown CCD message and payload | U | Compare stationary Park/Reverse/Neutral/Drive captures with wheels chocked, parking brake set, engine off where service procedure permits. Confirm repeatability and stale/loss behavior before allowing any P1 camera-trigger output. |
| OFF/LOW/HIGH selector | Known factory settings, electrical/message encoding unknown | U | Service wiring/troubleshooting and switch measurements |
| OEM radio diagnostics/periodic traffic | Unknown | U | Factory radio manual and isolated capture/bench study |

Elvira is a 2000 Plymouth Prowler. Use 1999 documentation for design with explicit carryover status; consult the owner's paper 2000 factory manual for critical wiring/electrical details as needed. Message encodings still require capture validation.
