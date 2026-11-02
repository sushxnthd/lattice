#!/usr/bin/env python3
"""Conditional scope gate for Run432's exact-int compiler.

Not an enforceable runtime attestation: absence of tracing now cannot
guarantee absence of frame mutation during future execution.
"""
import sys
from run432_pure_ir import Unknown,sha,transact

CLOSED='CLOSED_WORLD_NO_EXTERNAL_FRAME_MUTATION'
FINAL='FINAL_STORE_RETURN'

def certified_transaction(source,action,*,mode,observation,environment):
    if observation!=FINAL:
        raise Unknown('UNKNOWN_TRACE_OBSERVABILITY')
    if environment!=CLOSED:
        raise Unknown('UNKNOWN_EXTERNAL_FRAME_MUTATION')
    if sys.gettrace() is not None:
        raise Unknown('ACTIVE_TRACE_VIOLATES_ENVIRONMENT')
    output,receipt=transact(source,sha(source),action,mode)
    receipt['observation_scope']=FINAL
    receipt['environment_assumption']=CLOSED
    receipt['environment_verified']=False
    receipt['conditional_not_runtime_guarantee']=True
    return output,receipt
