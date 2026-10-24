#!/usr/bin/env python3
"""SHA-verified Run230 request reconstruction and raw Qwen inference."""
from __future__ import annotations
import argparse, hashlib, io, json, pathlib, tarfile, time, traceback, urllib.request

PREFIX=('Repair this two-file issue. You may replace ONLY the two create_gif methods. '
'Both conditions have exactly the same source facts, edit authority, compiler and verifier. '
'Return one JSON object with exactly TWO actions, one per file. Each action has '
'EXACTLY five fields: op,path,file_sha256,selector,replacement. '
'op must be replace. Copy path and file_sha256 exactly. '
'selector MUST be the supplied 24-character target_id for that method. '
'replacement MUST be the COMPLETE Python method source, starting with four spaces followed '
'by def create_gif(...), retaining the method signature and correct indentation. '
'Do not put the target_id in replacement. Do not return a method body alone. '
'There is NO content field. Do not create or delete files. '
'On unsolved objects, including empty or partially solved BatchStudy simulations, '
'raise ValueError before any QuickPlot construction or GIF generation. '
'For fully solved objects preserve GIF creation, cached QuickPlot and all arguments. '
'Do not use markdown or commentary.\nISSUE:\n')

def canonical(o):return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def schema():
    a={'type':'object','properties':{'op':{'type':'string','enum':['replace']},
        'path':{'type':'string'},'file_sha256':{'type':'string'},
        'selector':{'type':'string'},'replacement':{'type':'string'}},
        'required':['op','path','file_sha256','selector','replacement'],
        'additionalProperties':False}
    return {'type':'json_schema','json_schema':{'name':'lattice_replace_only_five_field_v1',
        'strict':True,'schema':{'type':'object','properties':{
        'actions':{'type':'array','minItems':2,'maxItems':2,'items':a}},
        'required':['actions'],'additionalProperties':False}}}

def restore(old_tar,out,prereg):
    out.mkdir(parents=True,exist_ok=True)
    freeze=json.loads(prereg.read_text())
    assert freeze['protocol']=='K-SYNTH-1/run230-five-field-schema-feasibility-v1'
    assert freeze['status']=='prospectively_frozen_before_inference'
    assert freeze['schema_sha256']==sha(canonical(schema()))
    old=old_tar.read_bytes()
    assert sha(old)=='f621b5d6e98df91b277dd5528e7f15af32708b302c997520aa83063fb2c4ff3a'
    with tarfile.open(fileobj=io.BytesIO(old),mode='r:gz') as tar:
        members={x.name:tar.extractfile(x).read() for x in tar.getmembers() if x.isfile()}
    for arm in freeze['arms']:
        req=json.loads(members[arm+'-request.json'])
        old_prompt=req['messages'][0]['content']
        _,body=old_prompt.split('\nISSUE:\n',1)
        issue,view=body.split('\nSOURCE_FACTS:\n',1)
        req['messages'][0]['content']=PREFIX+issue+'\nSOURCE_FACTS:\n'+view
        req['response_format']=schema()
        data=canonical(req)
        assert sha(data)==freeze['request_sha256'][arm],(arm,sha(data))
        assert sha(req['messages'][0]['content'].encode())==freeze['prompt_sha256'][arm]
        assert req['model']==freeze['model'] and req['seed']==freeze['seed']
        assert req['temperature']==freeze['temperature'] and req['max_tokens']==freeze['max_tokens']
        (out/(arm+'-request.json')).write_bytes(data)
    (out/'run230-preregistration.json').write_bytes(prereg.read_bytes())
    print('RESTORE VERIFIED',freeze['request_sha256'],flush=True)

def infer(out,endpoint):
    freeze=json.loads((out/'run230-preregistration.json').read_text())
    for arm in freeze['arms']:
        request_bytes=(out/(arm+'-request.json')).read_bytes()
        rec={'arm':arm,'request_sha256':sha(request_bytes),
             'model_sha256':freeze['model_gguf_sha256'],
             'seed':freeze['seed'],'temperature':freeze['temperature'],
             'max_tokens':freeze['max_tokens']}
        try:
            start=time.monotonic()
            raw=urllib.request.urlopen(urllib.request.Request(endpoint,data=request_bytes,
                headers={'Content-Type':'application/json'},method='POST'),timeout=3600).read(4000000)
            (out/(arm+'-response.json')).write_bytes(raw)
            response=json.loads(raw)
            rec.update(response_sha256=sha(raw),model_reported=response.get('model'),
                usage=response.get('usage'),finish_reason=response['choices'][0].get('finish_reason'),
                output_text=response['choices'][0]['message'].get('content'),
                elapsed_seconds=time.monotonic()-start)
        except Exception as exc:rec.update(error=repr(exc),traceback=traceback.format_exc())
        (out/(arm+'-inference-record.json')).write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n')
        print(arm,rec.get('usage'),rec.get('error','completed'),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--restore',action='store_true');p.add_argument('--infer',action='store_true')
    p.add_argument('--old-tar',type=pathlib.Path);p.add_argument('--prereg',type=pathlib.Path)
    p.add_argument('--out',type=pathlib.Path,required=True)
    p.add_argument('--endpoint',default='http://127.0.0.1:8080/v1/chat/completions')
    a=p.parse_args()
    if a.restore:restore(a.old_tar,a.out,a.prereg)
    if a.infer:infer(a.out,a.endpoint)
