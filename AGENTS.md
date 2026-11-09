# Engineering rules

- Treat the vehicle bus as safety-critical. Default to receive-only and physically inhibit transmit.
- Never connect to the vehicle until the interface is high impedance, protected, and validated on a bench.
- No unverified bias, termination, frame identifiers, signal encodings, or radio behavior. Label confidence and cite evidence.
- Distinguish CCD from PCI/J1850 VPW; do not reuse physical layers or timings across them.
- Keep transport, framing, decoding, events, and outputs separate. Use bounded buffers and explicit state machines.
- Synthetic captures must carry a synthetic marker and must never be described as measured vehicle data.
- No vehicle transmission, diagnostic replay, or irreversible wiring changes without explicit user authorization.
- Preserve upstream licenses. Do not incorporate copyleft source without resolving compatibility.
- Use deterministic host tests for parsing and control behavior. Do not claim vehicle validation from host tests.
- Track unknowns as issues and retain provenance in `docs/sources.md` and the signal dictionary.
