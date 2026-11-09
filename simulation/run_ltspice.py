"""Run or assess LTspice batch fixtures; require every expected measurement.

Vendor libraries remain local. Limits describe these synthetic experiments,
not qualification of a circuit for connection to a vehicle.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

LIMITS = {
    'buck': {'vout_light': (4.75, 5.25), 'vout_heavy': (4.75, 5.25),
             'vout_min': (4.5, 5.25), 'vout_max': (4.75, 5.5),
             'inductor_peak': (0.01, 1.5)},
    'rx_lt1716': {'rx_idle': (2.8, 3.5), 'rx_dominant': (-0.1, 0.4),
                  'rx_return': (2.8, 3.5),
                  'input_p_off': (-10e-6, 10e-6),
                  'input_n_off': (-10e-6, 10e-6)},
    'ccd_bus_lt1716': {'diff_idle': (-0.05, -0.005),
                       'diff_dominant': (0.2, 0.8),
                       'rx_idle': (2.8, 3.5), 'rx_dominant': (-0.1, 0.4),
                       'diff_inhibited': (-0.05, -0.005),
                       'rx_inhibited': (2.8, 3.5),
                       'drive_current': (0.001, 0.01)},
}


def assess(circuit: Path, limits_from: str | None = None) -> dict:
    log = circuit.with_suffix('.log').read_text(errors='replace')
    measurements = {m[0].lower(): float(m[1]) for m in re.findall(
        r'^([\w]+):[^\r\n]*?=\s*([-+\d.eE]+)', log, re.M)}
    checks = {}
    for name, (low, high) in LIMITS[limits_from or circuit.stem].items():
        value = measurements.get(name)
        checks[name] = {'value': value, 'min': low, 'max': high,
                        'pass': value is not None and low <= value <= high}
    completed = 'Total elapsed time:' in log
    passed = completed and all(check['pass'] for check in checks.values())
    result = {'netlist': circuit.name, 'synthetic': True,
              'netlist_sha256': hashlib.sha256(circuit.read_bytes()).hexdigest(),
              'simulator': log.splitlines()[0], 'completed': completed,
              'checks': checks, 'pass': passed}
    directory = circuit.parent / 'results'
    directory.mkdir(exist_ok=True)
    (directory / f'{circuit.stem}_ltspice.json').write_text(
        json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('circuit', type=Path)
    parser.add_argument('--assess-existing', action='store_true')
    parser.add_argument('--timeout', type=int, default=600)
    parser.add_argument('--limits-from', choices=list(LIMITS))
    parser.add_argument('--executable', type=Path,
                        default=Path(r'C:\Program Files\ADI\LTspice\LTspice.exe'))
    args = parser.parse_args()
    circuit = args.circuit.resolve()
    if not args.assess_existing:
        # Remove only this fixture's previous log, preventing stale success.
        circuit.with_suffix('.log').unlink(missing_ok=True)
        subprocess.run([str(args.executable), '-b', str(circuit)],
                       cwd=circuit.parent, timeout=args.timeout, check=True)
    result = assess(circuit, args.limits_from)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['pass'] else 1)
