# ADR 0004: CCD core with extensible DLC capture threads

Status: Accepted. P0 core is CCD-only and receive-only. Other DLC lines and full OBD-II behavior are stretch scope.

## Decision

P0 core implements receive-only capture of the Prowler CCD differential pair at the J1962 connector. Capture records carry a stable thread ID so independently validated physical layers can be added later. Candidate stretch channels from ChryslerScanner V2.1.0 include PCI/VPW and SCI conductors; these are not assumed populated on the Prowler and receive no P0-core hardware. Full OBD-II pass-through and diagnostic request/reply behavior are also stretch objectives, not gates for the first CCD capture.

The first web interface needs a CCD tab with raw and parsed frames, channel status, timing, and loss/error counters. As stretch channels are implemented, each gets its own tab and the shared timeline can compare them. Capture files preserve thread identity from the first release. Independent hardware edge inputs prevent unrelated bus activity from being collapsed into one serial stream.

## Rationale

One CCD receiver cannot capture single-wire PCI/VPW or SCI signaling. Preserving distinct thread identity now makes those future extensions straightforward without delaying the first Prowler CCD capture. The DLC may expose only some vehicle traffic; passive capture also cannot elicit replies that are sent only after a diagnostic request.

## Constraints

- P0 is passive at the vehicle connector. It has no transmit driver. Future isolated-bench/request-reply stages require separate review and physical inhibit; any vehicle transmission requires explicit user authorization.
- Do not connect a pin just because it is listed in a generic scanner reference. Confirm it on the Prowler first.
- Do not connect 12 V-capable lines directly to ESP32 pins. Each interface needs a reviewed input range, protection, loading, threshold and output-level design.
- No bias or termination on CCD, and no generic shared comparator circuit across protocols.
- As tabs are added, filtering is presentation-only; exported raw capture retains all enabled threads and overrun markers.

## Evidence

- ChryslerScanner V2.1.0 schematic's connector table assigns candidate CCD, PCI/VPW and SCI contacts; the project is GPL-3.0 and is used as a source of pin-map clues only.
- Macchina CCBDM20 manufacturer drawing describes a board-mount right-angle male J1962 connector, 16 contacts, dimensions in millimeters, and 30 V maximum rating. The exact connector footprint must be checked against the physical part before PCB release.
- Neither source proves the 1999 Prowler's complete DLC population. OEM service information and physical measurement remain required.
