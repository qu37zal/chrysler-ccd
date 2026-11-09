"""Compare the KiCad-exported netlist against every declared component pin."""
import json
from pathlib import Path
import sexpdata as sx

ROOT=Path(__file__).resolve().parents[1]/'kicad/p0_frontend'
parts=json.loads((ROOT/'components.json').read_text())
data=sx.load(open(ROOT/'p0_frontend.net',encoding='utf8'))
def field(node,key):
    return next(x for x in node if isinstance(x,list) and str(x[0])==key)
nets=field(data,'nets')
actual={}
for net in nets[1:]:
    # Root-sheet local labels are exported with a leading slash by KiCad.
    name=field(net,'name')[1].removeprefix('/')
    for node in net:
        if isinstance(node,list) and str(node[0])=='node':
            ref,pin=field(node,'ref')[1],field(node,'pin')[1]
            if not ref.startswith('#'):
                assert (ref,pin) not in actual, (ref,pin,'duplicated')
                actual[ref,pin]=name
expected={(p['ref'],pin):net for p in parts for pin,net in p['pins'].items()}
missing=set(expected)-set(actual)
extra=set(actual)-set(expected)
wrong={key:(net,actual.get(key)) for key,net in expected.items() if actual.get(key)!=net}
assert not (missing or extra or wrong), dict(missing=list(missing),extra=list(extra),wrong=wrong)
print(f'PASS: {len(parts)} components, {len(expected)} pin connections, {len(nets)-1} nets match the source.')
