#!/usr/bin/env python3
"""Stop hook: before the turn ends, make sure docs/02-requirements is still clean.

Why a Stop hook and not PostToolUse: a requirements change touches several files,
and the tree is legitimately broken between the first edit and the last one. A
per-edit hook would complain about errors that the next edit was about to fix.
This runs once, when the turn ends.

What it does, in order:
1. If `stop_hook_active` is true, allow the stop. This is the documented loop
   guard: Claude Code is already continuing because of this hook, so blocking
   again could loop. (Claude Code also caps continuations at 8.)
2. If nothing under docs/02-requirements/ changed, allow the stop.
3. Otherwise run `reqcheck check`. On errors, block the stop and hand the errors
   back so they get fixed.

Works on Windows (Git Bash) and Linux: reqcheck runs with the same interpreter
that runs this script, and git is called without a shell.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

REQ_PATH = "docs/02-requirements"


def _utf8(stream):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def allow():
    """Say nothing. The turn ends normally."""
    return 0


def block(reason):
    json.dump({"decision": "block", "reason": reason}, sys.stdout)
    sys.stdout.write("\n")
    return 0


def run(args, cwd):
    return subprocess.run(
        args, cwd=str(cwd), capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )


def requirements_changed(root):
    """True if anything under docs/02-requirements/ is dirty.

    Returns True when git cannot answer, so an unreadable state does not
    silently switch the check off.
    """
    try:
        proc = run(["git", "status", "--porcelain", "--", REQ_PATH], root)
    except OSError:
        return True
    if proc.returncode != 0:
        return True
    return bool(proc.stdout.strip())


def main():
    _utf8(sys.stdout)
    _utf8(sys.stderr)
    try:
        data = json.load(sys.stdin)
    except (ValueError, OSError):
        return allow()
    if not isinstance(data, dict):
        return allow()

    # 1. Loop guard.
    if data.get("stop_hook_active") is True:
        return allow()

    root = os.environ.get("CLAUDE_PROJECT_DIR")
    root = Path(root) if root else Path(__file__).resolve().parent.parent
    script = root / "tools" / "reqcheck.py"
    if not script.is_file():
        return allow()

    # 2. Did the requirements change?
    if not requirements_changed(root):
        return allow()

    # 3. Check them.
    try:
        proc = run([sys.executable, str(script), "check"], root)
    except OSError as exc:
        return block("reqcheck could not run: %s. Check it by hand before you finish." % exc)

    if proc.returncode == 0:
        return allow()

    return block(
        "docs/02-requirements/ changed in this turn and reqcheck reports errors. "
        "Fix every ERROR below, then finish.\n\n"
        + (proc.stdout or "")
        + (proc.stderr or "")
    )


if __name__ == "__main__":
    sys.exit(main())
