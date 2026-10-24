#!/usr/bin/env python3
"""Run one POSIX command with a deadline; embedded in the owned sandbox by qualification.py."""
import json
import os
import signal
import subprocess
import sys
import time

GRACE_SECONDS = 5


def supervise(command, seconds, control_id):
    started = time.monotonic()
    common = {'type': 'agentos.run_control', 'version': 1,
              'control_id': control_id, 'timeout_seconds': seconds,
              'grace_seconds': GRACE_SECONDS}

    def emit(**fields):
        # A child may leave a partial line. Preserve it without joining the control event.
        print('\n' + json.dumps(dict(common, **fields)), flush=True)

    try:
        child = subprocess.Popen(command, start_new_session=True)
    except OSError as error:
        emit(phase='launch_failed', error=str(error), elapsed_seconds=time.monotonic() - started)
        return 127
    timed_out = False
    signals = []

    def interrupted(signum, frame):
        raise SystemExit(128 + signum)

    signal.signal(signal.SIGTERM, interrupted)

    def send(sig):
        try:
            os.killpg(child.pid, sig)
            signals.append(sig.name)
        except ProcessLookupError:
            pass

    try:
        emit(phase='started', pid=child.pid, process_group=child.pid)
        child.wait(timeout=max(0, seconds - (time.monotonic() - started)))
    except subprocess.TimeoutExpired:
        timed_out = True
        send(signal.SIGINT)
        try:
            child.wait(timeout=GRACE_SECONDS)
        except subprocess.TimeoutExpired:
            send(signal.SIGKILL)
            child.wait()
        # A descendant may ignore SIGINT even when the CLI exits gracefully.
        # Only the new command process group is addressed; escaped groups are not covered.
        if 'SIGKILL' not in signals:
            send(signal.SIGKILL)
    except BaseException:
        # Do not leave our command running if this supervisor is interrupted.
        send(signal.SIGKILL)
        child.wait()
        raise
    exit_code = 124 if timed_out else (child.returncode if child.returncode >= 0 else 128 - child.returncode)
    emit(phase='finished', pid=child.pid, process_group=child.pid,
         timed_out=timed_out, signals=signals, child_returncode=child.returncode,
         exit_code=exit_code, elapsed_seconds=time.monotonic() - started)
    return exit_code


if __name__ == '__main__':
    seconds = int(sys.argv[1])
    if not 1 <= seconds <= 86400 or len(sys.argv) < 4:
        raise SystemExit('expected timeout seconds 1..86400, control ID and command')
    raise SystemExit(supervise(sys.argv[3:], seconds, sys.argv[2]))
