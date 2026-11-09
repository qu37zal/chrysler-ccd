# ADR 0001: Layer boundaries and receive-only default

Status: Accepted

The code separates physical transport, frame representation, interpretation, vehicle events and output policy. P0 has no transmit driver path enabled. Unknown vehicle signals stay unknown until source-backed validation. This constrains accidental transmission and permits host-side replay without hardware.
