---
name: req-change
description: Add, edit, split, merge or withdraw an actor, problem, use case or requirement in docs/02-requirements. Finds every item above and below the change (and IDs used in code, tests, ADRs), shows the impact, then updates all affected items together, not just the one asked for.
when_to_use: Use whenever any file in docs/02-requirements must change, even a one-word fix. Also use when the user asks "what happens if we change X" about a requirement.
paths: docs/02-requirements/**
argument-hint: "[ID or short description of the change]"
allowed-tools: Read Grep Glob Edit Bash(python3 tools/reqcheck.py *) Bash(python tools/reqcheck.py *)
---

# Change requirements safely

Requested change: $ARGUMENTS

Follow the six steps in [docs/02-requirements/AGENTS.md](../../../docs/02-requirements/AGENTS.md): impact → propose → approve → apply → check → journal. That file owns the procedure, the chain and the journal format. Read it first, with the **Writing rules** of each file you may touch and [id-lifecycle.md](../../../docs/02-requirements/id-lifecycle.md). Do not copy those rules into your answer; follow them.

This file adds only the mechanics for each step.

## Before step 1 · Find what the user means

1. If the request does not name an ID, search for it and confirm with the user.
2. Decide the type of change with the test in `id-lifecycle.md`: add, wording change, meaning change, withdraw, split or merge.
3. If you are not sure whether it is wording or meaning, **ask the user**. Do not guess.

## Step 1 · Impact

1. Run `impact` for each affected ID. For a new item, run it on each item the new one will point to.
2. Read each result against [reference/impact-map.md](reference/impact-map.md): ABOVE, BELOW, MENTIONED BY and OUTSIDE.
3. Also check `docs/01-glossary/01-glossary.md`: does the change use a term that is not there?

## Step 2 · Propose

Show one table. Do not edit any file yet.

| ID  | File | Change                                   | Reason             |
| --- | ---- | ---------------------------------------- | ------------------ |
| …   | …    | add / edit / withdraw / no change needed | one short sentence |

Below the table, list:

1. **Coverage after the change**: any problem, use case or actor that will lose its cover, and how you fix it.
2. **Outside the requirements folder**: tests, code, ADRs, experiment reports that mention the IDs. You only **list** these. You do not edit code or accepted ADRs.
3. **Vision or scope**: say so if the change adds or removes scope. Do not edit `docs/00-vision/00-vision.md` without approval.
4. **Open questions**: anything the user must decide.

## Step 3 · Approve — stop here

Wait for the user to approve, change or reject. Do not continue on your own.

## Step 4 · Apply

Add new glossary terms if the change needs them.

## Step 6 · Journal, then finish

After the journal entry, tell the user in a few lines:

- what changed;
- the check result (errors and warnings);
- what is left for them to do by hand.
