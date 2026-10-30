"""Prospectively specified asyncio-backend behavioral oracle for AnyIO PR #595.
Run as a standalone Python process with historical package on PYTHONPATH.
All case outcomes are recorded; the test does not patch implementation or inspect reference diff.
"""
import asyncio
import hashlib
import json
import os
import pathlib
import sys
import traceback
import anyio

async def event_cancel_after_set():
    event = anyio.Event()
    woke = []
    async def setter(tg):
        event.set()
        tg.cancel_scope.cancel()
    async with anyio.create_task_group() as tg:
        tg.start_soon(setter, tg)
        await event.wait()
        woke.append('yes')
    assert woke == ['yes'], woke

async def event_cancel_after_set_nested():
    event = anyio.Event()
    woke = []
    async def setter(outer):
        event.set()
        outer.cancel_scope.cancel()
    async with anyio.create_task_group() as outer:
        async with anyio.create_task_group() as inner:
            outer.start_soon(setter, outer)
            await event.wait()
            woke.append('yes')
    assert woke == ['yes'], woke

async def event_cancel_after_set_shielded():
    event = anyio.Event()
    woke = []
    async def setter(tg):
        event.set()
        tg.cancel_scope.cancel()
    async with anyio.create_task_group() as tg:
        tg.start_soon(setter, tg)
        with anyio.CancelScope(shield=True):
            await event.wait()
            woke.append('yes')
    assert woke == ['yes'], woke

async def memory_race(capacity):
    send, receive = anyio.create_memory_object_stream(capacity)
    got = []
    async def sender(tg):
        await send.send('payload')
        tg.cancel_scope.cancel()
    async with anyio.create_task_group() as tg:
        tg.start_soon(sender, tg)
        value = await receive.receive()
        got.append(value)
    assert got == ['payload'], got

async def event_regular():
    event=anyio.Event()
    async def setter(): event.set()
    async with anyio.create_task_group() as tg:
        tg.start_soon(setter)
        await event.wait()
    assert event.is_set()

async def memory_buffered():
    send,receive=anyio.create_memory_object_stream(2)
    await send.send('x')
    assert await receive.receive() == 'x'

async def memory_rendezvous():
    send,receive=anyio.create_memory_object_stream(0)
    async with anyio.create_task_group() as tg:
        tg.start_soon(send.send, 'x')
        assert await receive.receive() == 'x'

async def blocked_receive_cancel():
    send,receive=anyio.create_memory_object_stream(0)
    got=[]
    async with anyio.create_task_group() as tg:
        async def reader():
            try:
                await receive.receive()
            except anyio.get_cancelled_exc_class():
                got.append('cancelled')
        tg.start_soon(reader)
        await anyio.sleep(0)
        tg.cancel_scope.cancel()
    assert got == ['cancelled'], got

async def stream_end():
    send,receive=anyio.create_memory_object_stream(1)
    await send.aclose()
    try:
        await receive.receive()
    except anyio.EndOfStream:
        return
    raise AssertionError('expected EndOfStream')

async def cancel_checkpoint():
    seen=[]
    with anyio.CancelScope() as scope:
        scope.cancel()
        try:
            await anyio.sleep(0)
        except anyio.get_cancelled_exc_class():
            seen.append('cancelled')
    assert seen == ['cancelled'], seen

CASES = [
    ('T1_event_cancel_after_set', event_cancel_after_set, 'target'),
    ('T2_event_cancel_after_set_nested', event_cancel_after_set_nested, 'target'),
    ('T3_event_cancel_after_set_shielded', event_cancel_after_set_shielded, 'target'),
    ('T4_memory_race_0', lambda: memory_race(0), 'target'),
    ('T5_memory_race_1', lambda: memory_race(1), 'target'),
    ('T6_memory_race_2', lambda: memory_race(2), 'target'),
    ('C1_event_regular', event_regular, 'control'),
    ('C2_memory_buffered', memory_buffered, 'control'),
    ('C3_memory_rendezvous', memory_rendezvous, 'control'),
    ('C4_blocked_receive_cancel', blocked_receive_cancel, 'control'),
    ('C5_stream_end', stream_end, 'control'),
    ('C6_cancel_checkpoint', cancel_checkpoint, 'control'),
]

def main():
    outcomes=[]
    for name,fn,kind in CASES:
        try:
            async def bounded():
                with anyio.fail_after(3):
                    await fn()
            anyio.run(bounded, backend='asyncio')
            outcomes.append({'name':name,'kind':kind,'passed':True,'error':None})
        except BaseException as exc:
            outcomes.append({'name':name,'kind':kind,'passed':False,
                             'error':f'{type(exc).__name__}: {str(exc)[:300]}'})
    out={'schema':'lattice.run362.anyio.v1','python':sys.version.split()[0],
         'anyio_path':str(pathlib.Path(anyio.__file__).resolve()),
         'outcomes':outcomes}
    print(json.dumps(out,sort_keys=True,indent=2))
    if len(outcomes)!=12:
        raise SystemExit(2)

if __name__=='__main__':main()
