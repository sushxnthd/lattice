#!/usr/bin/env python3
"""Standalone POSIX counterexample: recovery ignores active writer's flock.

The full Run439 archive tests original Run438 functions in 64 real processes.
This witness isolates the stage-removal/lock mechanism using stdlib only.
"""
import fcntl, pathlib, shutil, tempfile, threading, time

def demonstrate(lock_recovery):
    with tempfile.TemporaryDirectory() as tmp:
        root=pathlib.Path(tmp)
        (root/'LOCK').write_bytes(b'lock')
        stage=root/'staging'/'transaction'
        stage.mkdir(parents=True)
        ready=threading.Event();release=threading.Event()
        outcome=[];cleaned=[]
        def writer():
            with (root/'LOCK').open('rb') as f:
                fcntl.flock(f,fcntl.LOCK_EX)
                try:
                    (stage/'provider.py').write_text('first')
                    ready.set()
                    assert release.wait(3)
                    (stage/'consumer.py').write_text('second')
                    outcome.append('COMMITTED')
                except FileNotFoundError:
                    outcome.append('STAGE_DELETED')
                finally:fcntl.flock(f,fcntl.LOCK_UN)
        def recovery():
            with (root/'LOCK').open('rb') as f:
                if lock_recovery:fcntl.flock(f,fcntl.LOCK_EX)
                try:
                    if stage.exists():shutil.rmtree(stage)
                    cleaned.append(True)
                finally:
                    if lock_recovery:fcntl.flock(f,fcntl.LOCK_UN)
        wt=threading.Thread(target=writer);wt.start()
        assert ready.wait(3)
        rt=threading.Thread(target=recovery);rt.start()
        if not lock_recovery:
            rt.join(2);assert cleaned
        else:
            time.sleep(.02);assert not cleaned
        release.set();wt.join(3);rt.join(3)
        assert not wt.is_alive() and not rt.is_alive()
        return outcome[0]

if __name__=='__main__':
    unsafe=demonstrate(False)
    safe=demonstrate(True)
    assert (unsafe,safe)==('STAGE_DELETED','COMMITTED')
    print('unlocked_recovery='+unsafe+'; locked_recovery='+safe)
