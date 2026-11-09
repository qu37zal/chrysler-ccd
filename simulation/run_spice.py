"""Batch-run a netlist using KiCad's installed ngspice shared library.

Uses the standard library only. Vendor models are downloaded separately and
kept out of Git. Run each netlist in a fresh process so ngspice state is isolated.
"""
from __future__ import annotations
import argparse
import ctypes as ct
import json
import os
from pathlib import Path
import re

LIMITS = {
    'rx': {'rx_idle': (2.8, 3.5), 'rx_dominant': (-0.1, 0.4), 'rx_return': (2.8, 3.5)},
    'ldo': {'vout_light': (3.2, 3.4), 'vout_heavy': (3.2, 3.4),
            'vout_min': (3.1, 3.4), 'vout_max': (3.2, 3.5)},
    'ccd_bus': {'diff_idle': (-0.05, -0.005), 'diff_dominant': (0.2, 0.8),
                'rx_idle': (2.8, 3.5), 'rx_dominant': (-0.1, 0.4),
                'diff_inhibited': (-0.05, -0.005), 'rx_inhibited': (2.8, 3.5),
                'drive_current': (-0.01, -0.001)},
    'buck': {'vout_light': (4.75, 5.25), 'vout_heavy': (4.75, 5.25),
             'vout_min': (4.5, 5.25), 'vout_max': (4.75, 5.5),
             'inductor_peak': (0.01, 1.5)},
}


def run(circuit: Path, kicad: Path, vectors: list[str]) -> dict:
    circuit = circuit.resolve()
    handles = [os.add_dll_directory(str(kicad / p)) for p in ['bin', 'lib/ngspice']]
    lib = ct.CDLL(str(kicad / 'bin/ngspice.dll'))
    messages = []

    @ct.CFUNCTYPE(ct.c_int, ct.c_char_p, ct.c_int, ct.c_void_p)
    def output(message, _ident, _user):
        messages.append(message.decode(errors='replace'))
        return 0

    lib.ngSpice_Init.argtypes = [ct.c_void_p] * 7
    lib.ngSpice_Init(ct.cast(output, ct.c_void_p), None, None, None, None, None, None)
    lib.ngSpice_Command.argtypes = [ct.c_char_p]
    def command(text):
        return lib.ngSpice_Command(text.encode())

    # ngspice's codemodel parser retains quotes around Windows file names.
    # A Windows short path avoids spaces without copying DLLs or changing PATH.
    for model in sorted((kicad / 'lib/ngspice').glob('*.cm')):
        short = ct.create_unicode_buffer(4096)
        if not ct.windll.kernel32.GetShortPathNameW(str(model), short, len(short)):
            raise OSError(f'Cannot resolve code-model path: {model}')
        command('codemodel ' + short.value.replace('\\', '/'))
    os.chdir(circuit.parent)
    result_dir = Path('results')
    result_dir.mkdir(exist_ok=True)
    for text in ['set ngbehavior=ps', 'set noaskquit', 'set numdgt=12',
                 'source ' + circuit.name, 'run']:
        command(text)
    errors = [s for s in messages if re.search(r'\b(error|fatal|aborted)\b|timestep too small', s, re.I)]
    if vectors and not errors:
        command('set wr_vecnames')
        command('set wr_singlescale')
        command(f'wrdata results/{circuit.stem}.txt ' + ' '.join(vectors))
    Path(f'results/{circuit.stem}.log').write_text('\n'.join(messages), encoding='utf-8')
    measurements = {}
    for line in messages:
        match = re.match(r'stdout ([\w]+)\s*=\s*([-+\d.eE]+)', line)
        if match:
            measurements[match[1]] = float(match[2])
    result = {'netlist': circuit.name, 'synthetic': True,
              'simulator': next((s for s in messages if 'ngspice-' in s), ''),
              'errors': errors, 'measurements': measurements}
    result['checks'] = {name: {'value': measurements.get(name), 'min': low, 'max': high,
                        'pass': name in measurements and low <= measurements[name] <= high}
                        for name, (low, high) in LIMITS[circuit.stem].items()}
    result['pass'] = not errors and all(check['pass'] for check in result['checks'].values())
    Path(f'results/{circuit.stem}.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('circuit', type=Path)
    parser.add_argument('--kicad', type=Path, default=Path(r'C:\Program Files\KiCad\10.0'))
    parser.add_argument('--vectors', nargs='*', default=[])
    args = parser.parse_args()
    result = run(args.circuit, args.kicad, args.vectors)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['pass'] else 1)
