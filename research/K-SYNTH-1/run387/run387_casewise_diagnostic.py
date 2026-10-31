#!/usr/bin/env python3
"""Post-freeze diagnostic only: casewise exceptions and successes, not original oracle."""
import json,sys
from rich.console import Console
from rich.cells import cell_len
from run387_rich_oracle import CASES

records=[]
for group,name,source,width in CASES:
    try:
        console=Console(width=width,force_terminal=False,color_system=None,
                        highlight=False,legacy_windows=False)
        with console.capture() as capture: console.print(source)
        output=capture.get()
        lines=output.rstrip('\n').split('\n')
        ok=''.join(lines)==source and all(cell_len(line)<=width for line in lines)
        records.append({'group':group,'name':name,'passed':ok,'rendered':output,
                        'failure_kind':None if ok else 'INVARIANT_FAILED'})
    except Exception as e:
        records.append({'group':group,'name':name,'passed':False,
                        'failure_kind':type(e).__name__,'error':str(e)})
print(json.dumps({'records':records,'summary':{g:sum(r['passed'] for r in records if r['group']==g)
    for g in ('target_public','target_heldout','control')}},ensure_ascii=False,indent=2))
