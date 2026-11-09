# ADR 0004: P0 independent DLC capture threads

Status: Accepted as a capture architecture; physical pin assignments and electrical circuits remain provisional pending Prowler-specific validation.

## Decision

P0 shall treat every confirmed data conductor exposed at the J1962 connector as an independent capture thread. Initial candidate groups, based on ChryslerScanner V2.1.0's connector table, are the CCD differential pair (3/11), PCI/VPW (2), and the six SCI conductors (6/7/9/12/14/15). Each conductor or differential pair gets a protocol-specific receive front end and dedicated MCU capture input. Pin numbers and signal names remain candidate metadata until checked against 1999 Prowler service literature and the actual connector.

The web interface shall provide a tab per thread, with raw and parsed events, channel status, timing, and loss/error counters. A shared timeline permits cross-thread comparison. Capture files preserve thread identity on every event. Independent hardware timestamps/edge inputs prevent unrelated bus activity from being collapsed into one serial stream.

## Rationale

One CCD receiver cannot capture single-wire PCI/VPW or SCI electrical signaling. The connector can expose multiple physical layers while not exposing every in-vehicle network. Separate threads preserve signal integrity, protocol timing and source identity and allow later analysis to compare the threads.

## Constraints

- P0 is passive at the vehicle connector. All transmit drivers, if designed for isolated bench experiments, remain unpopulated and behind a normally-open physical inhibit.
- Do not connect a pin just because it is listed in a generic scanner reference. Confirm it on the Prowler first.
- Do not connect 12 V-capable lines directly to ESP32 pins. Each interface needs a reviewed input range, protection, loading, threshold and output-level design.
- No bias or termination on CCD, and no generic shared comparator circuit across protocols.
- Web tabs filter presentation only; exported raw capture retains all threads and overrun markers.

## Evidence

- ChryslerScanner V2.1.0 schematic's connector table assigns candidate CCD, PCI/VPW and SCI contacts; the project is GPL-3.0 and is used as a source of pin-map clues only.
- Macchina CCBDM20 manufacturer drawing describes a board-mount right-angle male J1962 connector, 16 contacts, dimensions in millimeters, and 30 V maximum rating. The exact connector footprint must be checked against the physical part before PCB release.
- Neither source proves the 1999 Prowler's complete DLC population. OEM service information and physical measurement remain required.
