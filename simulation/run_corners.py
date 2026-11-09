"""Deterministic synthetic CCD supply/bench-load corner sweep in LTspice."""
import itertools
import json
from pathlib import Path
import subprocess
from run_ltspice import assess

ROOT=Path(__file__).resolve().parent
base=(ROOT/'ccd_bus_lt1716.cir').read_text()
results=[]
for voltage,termination,capacitance in itertools.product([4.7,5.15],[60,120],['1n','20n']):
    name=f'.corner_{voltage}_{termination}_{capacitance}'
    path=ROOT/(name+'.cir')
    params=dict(VDRIVE=voltage,TERMINATION=termination,BUSCAP=capacitance)
    text=base.replace('.param VDRIVE=4.7 TERMINATION=120 BUSCAP=5n',
        f'.param VDRIVE={voltage} TERMINATION={termination} BUSCAP={capacitance}')
    path.write_text(text)
    path.with_suffix('.log').unlink(missing_ok=True)
    subprocess.run([r'C:\Program Files\ADI\LTspice\LTspice.exe','-b',str(path)],
                   cwd=ROOT,timeout=60,check=True)
    result=assess(path,'ccd_bus_lt1716')
    result['parameters']=params
    results.append(result)
    print(params, 'PASS' if result['pass'] else 'FAIL',flush=True)
output=dict(synthetic=True,scope='Nominal models; external bench loads, not asserted vehicle limits',
            pass_all=all(r['pass'] for r in results),cases=results)
(ROOT/'results/ccd_corners.json').write_text(json.dumps(output,indent=2)+'\n')
raise SystemExit(0 if output['pass_all'] else 1)
