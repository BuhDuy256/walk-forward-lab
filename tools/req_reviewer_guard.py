#!/usr/bin/env python3
"""PreToolUse guard for the req-reviewer subagent.

The subagent frontmatter cannot limit Bash to one command: a `tools` entry names
a whole tool, and a `disallowedTools` entry with a specifier removes the whole
tool. So the limit is enforced here instead, as a PreToolUse hook scoped to that
one subagent.

Two jobs:
1. Bash / PowerShell: allow only `tools/reqcheck.py`. Deny everything else.
2. Edit / Write / NotebookEdit: allow only files inside the agent's own memory
   directory. Setting `memory:` turns Read, Write and Edit on automatically, so
   the reviewer must be stopped from editing requirement files.

Deny is returned as a PreToolUse `permissionDecision`, so Claude sees the reason.
"""
import json
import re
import sys

MEMORY_DIR = "/.claude/agent-memory/req-reviewer/"

# Shell syntax that could chain a second command onto an allowed one.
CHAINING = ("&", "|", ";", "`", "$(", ">", "<", "\n", "\r")

# An ID, copied from ID_RE in tools/reqcheck.py so the two stay in step.
ID = r"(?:FR-[A-Z]{2}|NFR|CON|DR|UC|A|P)-\d{2}"

# `python tools/reqcheck.py check` or `... impact <ID>`, and nothing else.
# `python`, `python3` and `py` are all accepted, because python3 is often
# missing on Windows and python is often missing on Linux.
# Separators are normalised to "/" before matching, so Windows paths fit too.
# "-" comes first in every class: after a backslash it would read as a range.
ALLOWED_BASH = re.compile(
    r"^\s*"
    r"[-\w.:/ ]*?(?:python3?|py)(?:\.exe)?[\"']?"   # optional path + interpreter
    r"\s+[\"']?(?:\./)?(?:[-\w.:/]*/)?"             # optional path to the script
    r"tools/reqcheck\.py[\"']?"
    r"\s+(?:check|impact\s+" + ID + r")"
    r"\s*$"
)


def deny(reason):
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        },
        sys.stdout,
    )
    sys.stdout.write("\n")
    return 0


def main():
    try:
        data = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    if not isinstance(data, dict):
        return 0

    tool = data.get("tool_name") or ""
    tool_input = data.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return 0

    if tool in ("Bash", "PowerShell"):
        command = tool_input.get("command") or ""
        normalised = command.replace("\\", "/")
        if any(t in command for t in CHAINING) or not ALLOWED_BASH.match(normalised):
            return deny(
                "req-reviewer may run only tools/reqcheck.py. Use "
                "`python tools/reqcheck.py check` or "
                "`python tools/reqcheck.py impact <ID>` from the repository root, "
                "with no pipes, redirects or chained commands. "
                "Use Read, Grep and Glob for everything else."
            )
        return 0

    if tool in ("Edit", "Write", "NotebookEdit"):
        path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
        # On Windows the path arrives with backslashes, even under Git Bash.
        if MEMORY_DIR not in path.replace("\\", "/"):
            return deny(
                "req-reviewer is a reviewer: it reports problems and never edits "
                "project files. The only writable place is "
                ".claude/agent-memory/req-reviewer/. Put the finding in your report "
                "instead, and leave the fix to /req-change."
            )
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
