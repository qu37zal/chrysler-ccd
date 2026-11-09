# Synthetic analog validation

All stimuli here are synthetic. None is a Prowler capture or evidence of vehicle
compatibility. The leading receive candidate is LT1716 powered from 3.3 V.

## Reproduce

Populate the ignored local model cache as described in `models/README.md`.
On this machine LTspice 26.1.1 and KiCad 10.0.7/ngspice 46 are installed.
The runners use Python's standard library only.

```powershell
python simulation/run_ltspice.py simulation/rx_lt1716.cir
python simulation/run_ltspice.py simulation/ccd_bus_lt1716.cir
python simulation/run_corners.py
python simulation/run_ltspice.py simulation/buck.cir
python simulation/run_spice.py simulation/ldo.cir
```

The LM5164 test took approximately five minutes in LTspice. Each runner requires
all expected measurements to fall within stated limits. A solver completing a
transient run alone is not a passing result. `--assess-existing` explicitly
reassesses an existing LTspice log; ordinary runs delete the prior fixture log
first. Large waveforms and vendor libraries stay out of Git.

## Recorded findings, 2026-11-09

| Fixture | Result | Meaning and limits |
|---|---|---|
| `rx_lt1716.cir` | Pass: RX 3.300 V idle / 0.132 V dominant; nominal off-power input currents below 2 nA | Differential polarity and output logic are plausible. The model's off-power currents must not replace the datasheet's microamp input-bias envelope or physical measurement. |
| `ccd_bus_lt1716.cir` | Pass: about 0.463 V dominant differential; about 5.44 mA total driver-rail current; inhibited differential about −23 mV | A **floating** transmit supply with its 100 kΩ bleed is tested using an open switch. An asserted TX command cannot change the synthetic recessive state after the jumper opens. Total rail current includes gate drive, not just bus current. |
| `run_corners.py` | 8/8 pass | 4.7/5.15 V drive rail × 60/120 Ω external bench termination × 1/20 nF per-line capacitance. These are exploratory fixture loads, not verified vehicle extrema. Component tolerances, temperature, faults, arbitration and byte timing are not covered. |
| `buck.cir` in LTspice | Pass: 5.137/5.134 V average at light/heavy load; 5.001–5.168 V during the load step; 0.831 A peak inductor current | 14 V synthetic input; roughly 0.1→0.6 A load. LM5164-Q1, 68 µH inductor and Type-3 ripple network. This does not test the input fuse/TVS/reverse-battery network or crank/load dump. Feedback/ripple offset needs optimization before final rail selection. |
| `ldo.cir` in ngspice | Pass: 3.303/3.302 V average; 3.264–3.341 V during load transitions | TLV76701, 4.7 V input, roughly 0.1→0.5 A load. PCB thermal performance remains untested. |
| `buck.cir` in ngspice | Failed: output does not regulate | Simulator/model compatibility issue remains unresolved. Use the recorded LTspice result for this candidate; do not change vendor internals merely to force a pass. |

`rx.cir`, `ccd_frontend.lib`, and `ccd_bus.cir` retain the earlier TLV1701
exploration. The positive clamps in that old frontend can load an unpowered bus
tap. They are **not** the current schematic or an approved vehicle interface.

## Next physical and electrical checks

1. Complete ground-referenced positive transient protection without creating an
   unpowered path into the local logic rails. Check input resistor pulse ratings.
2. Measure powered/unpowered input loading with weak synthetic bus bias. Use
   datasheet leakage bounds, device offsets, temperature and tolerances.
3. Exercise UART-like bytes at 7812.5 bit/s, shallow differentials, chatter,
   simultaneous drive/arbitration, stuck GPIO, brownout and all reset states.
4. Validate the actual protected power path, voltage corners, reverse battery,
   load steps, switch-node ringing and thermal rise before layout release.
5. Keep the transmit-power jumper absent for the first vehicle capture. This
   software work does not authorize any vehicle transmission.
