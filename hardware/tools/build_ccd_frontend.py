"""Generate the review schematic and purchase exports from one component list.

Requires sexpdata. Uses installed KiCad library symbols (CC-BY-SA with the
KiCad library exception). This is a subsystem schematic, not a released PCB.
"""
from __future__ import annotations
import copy
import csv
import json
from pathlib import Path
import uuid
import sexpdata as sx

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'hardware/kicad/p0_frontend'
LIB = Path(r'C:\Program Files\KiCad\10.0\share\kicad\symbols')
S = sx.Symbol


def uid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'chrysler-ccd/p0-frontend/' + name))


def form(key, *values):
    return [S(key), *values]


def child(node, key):
    return next(x for x in node if isinstance(x, list) and str(x[0]) == key)


def symbol(library, name):
    data = sx.load(open(LIB / (library + '.kicad_sym'), encoding='utf8'))
    entries = {x[1]: x for x in data if isinstance(x, list) and str(x[0]) == 'symbol'}
    def resolve(key):
        original = copy.deepcopy(entries[key])
        parent = next((x for x in original if isinstance(x, list) and str(x[0]) == 'extends'), None)
        if parent:
            inherited = resolve(parent[1])
            overrides = {x[1]: x for x in original if isinstance(x, list) and str(x[0]) == 'property'}
            original = [x for x in original if not isinstance(x, list) or str(x[0]) not in ('extends', 'property')]
            original += [copy.deepcopy(x) for x in inherited[2:] if isinstance(x, list) and str(x[0]) == 'symbol']
            original += list(overrides.values())
        for item in original:
            if isinstance(item, list) and str(item[0]) == 'symbol':
                suffix = item[1].rsplit('_', 2)[-2:]
                item[1] = name + '_' + '_'.join(suffix)
        return original
    result = resolve(name)
    result[1] = library + ':' + name
    return result


def pin_defs(definition):
    for unit in definition:
        if isinstance(unit, list) and str(unit[0]) == 'symbol':
            for pin in unit:
                if isinstance(pin, list) and str(pin[0]) == 'pin':
                    yield child(pin, 'number')[1], child(pin, 'at')[1:]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    project=OUT/'p0_frontend.kicad_pro'
    if not project.exists():
        project.write_text('{}\n')
    parts = []
    def add(ref, value, lib, fp, pins, xy, mpn, manufacturer, model, note=''):
        parts.append(dict(ref=ref, value=value, library=lib, footprint=fp,
                          pins=pins, xy=xy, mpn=mpn, manufacturer=manufacturer,
                          model=model, note=note))
    def r(ref, val, a, b, xy, suffix):
        add(ref, val, 'Device:R', 'Resistor_SMD:R_0805_2012Metric',
            {'1':a, '2':b}, xy, 'RC0805FR-07'+suffix+'L', 'YAGEO', 'ideal R; 1% tolerance not yet swept')
    def c(ref, val, a, b, xy, mpn):
        add(ref, val, 'Device:C', 'Capacitor_SMD:C_0805_2012Metric',
            {'1':a, '2':b}, xy, mpn, 'KEMET', 'ideal C; package/ESR not included')
    add('U101','LT1716HS5#TRMPBF','Chrysler:LT1716','Package_TO_SOT_SMD:TSOT-23-5',
        {'1':'CCD_RX','2':'GND','3':'SENSE_N','4':'SENSE_P','5':'3V3'},
        (125,55),'LT1716HS5#TRMPBF','Analog Devices','LT1716, installed LTspice encrypted family model',
        'H grade -40..125 C. Generic H part is not the automotive #W orderable.')
    r('R101','47k','CCD_P','SENSE_P',(35,50),'47K')
    r('R102','47k','CCD_N','SENSE_N',(65,50),'47K')
    c('C101','22p','SENSE_P','GND',(35,85),'C0805C220J5GACTU')
    c('C102','22p','SENSE_N','GND',(65,85),'C0805C220J5GACTU')
    c('C103','100n','3V3','GND',(155,85),'C0805C104K5RACTU')
    r('R103','4.7k','3V3','CCD_RX',(155,50),'4K7')
    # Diode pin 1 is cathode, pin 2 is anode.
    for ref,k,a,xy in [('D101','TX_HI','PMOS_D',(45,135)),
                        ('D102','NMOS_D','TX_LO',(110,135)),
                        ('D103','SENSE_P','GND',(35,115)),
                        ('D104','SENSE_N','GND',(65,115))]:
        add(ref,'BAV21W-7-F','Device:D','Diode_SMD:D_SOD-123',{'1':k,'2':a},xy,
            'BAV21W-7-F','Diodes Incorporated','BAV21W vendor file; model named DI_BAV21WS; CJO patch',
            'Vendor file naming inconsistency is tracked; do not treat model leakage as guaranteed.')
    add('Q101','BSS84Q-7-F','Transistor_FET:Q_PMOS_GSD','Package_TO_SOT_SMD:SOT-23',
        {'1':'P_GATE','2':'VTX','3':'PMOS_D'},(45,170),'BSS84Q-7-F','Diodes Incorporated','BSS84Q vendor subcircuit')
    for ref,pins,xy in [('Q102',{'1':'N_GATE','2':'GND','3':'NMOS_D'},(110,170)),
                         ('Q103',{'1':'TX_DOM','2':'GND','3':'P_GATE'},(175,170))]:
        add(ref,'2N7002Q-7-F','Transistor_FET:Q_NMOS_GSD','Package_TO_SOT_SMD:SOT-23',pins,xy,
            '2N7002Q-7-F','Diodes Incorporated','2N7002Q vendor subcircuit')
    add('Q104','MMBT3906-7-F','Transistor_BJT:Q_PNP_BEC','Package_TO_SOT_SMD:SOT-23',
        {'1':'PNP_BASE','2':'VTX','3':'N_DRIVE'},(240,170),
        'MMBT3906-7-F','Diodes Incorporated','DI_MMBT3906 vendor model')
    r('R104','100k','TX_DOM','GND',(175,205),'100K')
    r('R105','10k','VTX','P_GATE',(45,205),'10K')
    r('R106','10k','P_GATE','PNP_BASE',(210,205),'10K')
    r('R107','100k','PNP_BASE','VTX',(240,205),'100K')
    r('R108','220','N_DRIVE','N_GATE',(275,205),'220R')
    r('R109','10k','N_GATE','GND',(110,205),'10K')
    r('R110','100k','VTX','GND',(310,205),'100K')
    r('R111','360','TX_HI','CCD_P',(45,245),'360R')
    r('R112','360','CCD_N','TX_LO',(110,245),'360R')
    add('JP101','TX POWER - REMOVE FOR P0','Connector_Generic:Conn_01x02',
        'Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',
        {'1':'5V','2':'VTX'},(310,170),'TSW-102-07-G-S','Samtec','open/closed ideal bench supply in simulation',
        'Populate header; leave shunt absent. Not an authorization to drive a vehicle.')
    definitions = {}
    for part in parts:
        key = part['library']
        if key == 'Chrysler:LT1716':
            continue
        if key not in definitions:
            definitions[key] = symbol(*key.split(':'))
    definitions['power:PWR_FLAG'] = symbol('power', 'PWR_FLAG')
    lt = '''(symbol "Chrysler:LT1716" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)
      (property "Reference" "U" (at 0 8.89 0) (effects (font (size 1.27 1.27))))
      (property "Value" "LT1716" (at 0 -8.89 0) (effects (font (size 1.27 1.27))))
      (symbol "LT1716_0_1" (rectangle (start -7.62 7.62) (end 7.62 -7.62)
        (stroke (width 0.254) (type default)) (fill (type background))))
      (symbol "LT1716_1_1" PINLIST))'''
    pins=[]
    for number,name,kind,x,y,ang in [('1','OUT','output',10.16,0,180),
        ('2','V-','power_in',0,-10.16,90),('3','IN+','input',-10.16,2.54,0),
        ('4','IN-','input',-10.16,-2.54,0),('5','V+','power_in',0,10.16,270)]:
        pins.append(f'(pin {kind} line (at {x} {y} {ang}) (length 2.54) (name "{name}" (effects (font (size 1.27 1.27)))) (number "{number}" (effects (font (size 1.27 1.27)))))')
    definitions['Chrysler:LT1716']=sx.loads(lt.replace('PINLIST',' '.join(pins)))
    local=copy.deepcopy(definitions['Chrysler:LT1716']);local[1]='LT1716'
    (OUT/'Chrysler.kicad_sym').write_text(sx.dumps([S('kicad_symbol_lib'),
        form('version',20241209),form('generator','kicad_symbol_editor'),local]),encoding='utf8')
    (OUT/'sym-lib-table').write_text('(sym_lib_table (version 7) (lib (name "Chrysler") (type "KiCad") (uri "${KIPRJMOD}/Chrysler.kicad_sym") (options "") (descr "Independent project symbols")))\n')
    rootid=uid('sheet')
    doc=[S('kicad_sch'),form('version',20250114),form('generator','eeschema'),
         form('uuid',rootid),form('paper','A3'),[S('lib_symbols'),*definitions.values()]]
    def text(value,x,y,size=1.27):
        doc.append(form('text',value,form('at',x,y,0),
            form('effects',form('font',form('size',size,size)),form('justify',S('left'))),form('uuid',uid(value))))
    text('CCD receiver and physically inhibited bench transmitter — circuit review',20,15,2.0)
    text('DRAFT: subsystem only. No bus bias or termination. J1962 / power / MCU are on other design blocks.',20,23)
    text('RX: CCD+ > CCD- produces LOW. 47k input impedance; no clamp to a local positive rail.',20,31)
    text('TX: active-high TX_DOM. JP101 absent disconnects the drive rail; both gates default OFF.',20,145)
    text('5V / 3V3 / GND are external supplies. CCD_P / CCD_N go to the protected vehicle connector block.',180,55)
    text('Vehicle transmission remains unauthorized. Synthetic model checks are not bench validation.',180,65)
    for part in parts:
        x,y=[round(round(v/1.27)*1.27,5) for v in part['xy']]
        part['xy']=[x,y]
        instid=uid(part['ref']); definition=definitions[part['library']]
        inst=[S('symbol'),form('lib_id',part['library']),form('at',x,y,0),form('unit',1),
              form('in_bom',S('yes')),form('on_board',S('yes')),form('dnp',S('no')),form('uuid',instid)]
        refx,refy,valx,valy=x+5,y-2,x+5,y+2
        if part['ref'].startswith(('Q','D','JP')):
            refx,refy,valx,valy=x+8,y-7,x+8,y+7
        if part['ref'].startswith('U'):
            refx,refy,valx,valy=x+2,y-13,x+2,y+15
        for name,value,px,py,hidden in [('Reference',part['ref'],refx,refy,False),
            ('Value',part['value'],valx,valy,False),('Footprint',part['footprint'],x,y,True),
            ('MPN',part['mpn'],x,y,True),('Manufacturer',part['manufacturer'],x,y,True)]:
            effects=form('effects',form('font',form('size',1.0,1.0)),form('justify',S('left')))
            if hidden: effects.append(form('hide',S('yes')))
            inst.append(form('property',name,value,form('at',px,py,0),effects))
        inst.append(form('instances',form('project','p0_frontend',form('path','/'+rootid,
                         form('reference',part['ref']),form('unit',1)))))
        doc.append(inst)
        for number,(px,py,angle) in pin_defs(definition):
            net=part['pins'][number]; ax=round(x+px,5); ay=round(y-py,5)
            dx,dy={0:(-5.08,0),180:(5.08,0),90:(0,5.08),270:(0,-5.08)}[angle]
            bx,by=round(ax+dx,5),round(ay+dy,5)
            doc.append(form('wire',form('pts',form('xy',ax,ay),form('xy',bx,by)),
                form('stroke',form('width',0),form('type',S('default'))),form('uuid',uid(part['ref']+'/'+number+'/wire'))))
            doc.append(form('label',net,form('at',bx,by,0),
                form('effects',form('font',form('size',1,1)),form('justify',S('right' if angle==0 else 'left'),S('bottom'))),
                form('uuid',uid(part['ref']+'/'+number+'/label'))))
    for index,net in enumerate(['3V3','GND','5V']):
        x=round((220+index*30)/1.27)*1.27; y=85.09; reference=f'#FLG0{index+1}'
        doc.append(form('symbol',form('lib_id','power:PWR_FLAG'),form('at',x,y,0),form('unit',1),
            form('in_bom',S('no')),form('on_board',S('yes')),form('dnp',S('no')),form('uuid',uid(reference)),
            form('property','Reference',reference,form('at',x,y,0),form('effects',form('font',form('size',1,1)),form('hide',S('yes')))),
            form('property','Value','PWR_FLAG',form('at',x,y-5.08,0),form('effects',form('font',form('size',1,1)))),
            form('instances',form('project','p0_frontend',form('path','/'+rootid,form('reference',reference),form('unit',1))))))
        doc.append(form('label',net,form('at',x,y,0),form('effects',form('font',form('size',1,1))),form('uuid',uid(reference+'/net'))))
    doc.append(form('sheet_instances',form('path','/',form('page','1'))))
    (OUT/'p0_frontend.kicad_sch').write_text(sx.dumps(doc),encoding='utf8')
    (OUT/'components.json').write_text(json.dumps(parts,indent=2)+'\n')
    bomdir=ROOT/'hardware/bom';bomdir.mkdir(exist_ok=True)
    grouped={}
    for part in parts:
        key=part['mpn']
        group=grouped.setdefault(key,dict(mpn=key,manufacturer=part['manufacturer'],refs=[],quantity=0))
        group['refs'].append(part['ref']); group['quantity']+=1
    for distributor in ['digikey','mouser']:
        with (bomdir/f'ccd_frontend_bench_{distributor}.csv').open('w',newline='',encoding='utf8') as f:
            writer=csv.writer(f)
            writer.writerow(['Manufacturer Part Number','Manufacturer','Quantity','Reference Designators'])
            for group in grouped.values():
                writer.writerow([group['mpn'],group['manufacturer'],group['quantity'],' '.join(group['refs'])])
    print(f'{len(parts)} parts, {len(grouped)} purchase lines; native schematic and bench BOM exports written.')


if __name__=='__main__':
    main()
