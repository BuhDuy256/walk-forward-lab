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

A requirement file is part of a chain: **Actors → Problems → Use cases → Spec**.
Links point **up** only. So changing one item can break items that you cannot see from it.
Your job is to change the **whole chain** correctly, not just the line the user pointed at.

Run all commands from the repository root. Use `python` instead of `python3` if `python3` is not found.

## Step 1 · Read the rules

1. Read the **Writing rules** section at the top of every file you may touch in `docs/02-requirements/`.
2. Read `docs/02-requirements/id-lifecycle.md`.
3. Do **not** copy these rules into your answer. Follow them.

## Step 2 · Understand the request

1. Find the item(s) the user means. If the request does not name an ID, search for it and confirm with the user.
2. Decide the type of change, using the test in `docs/02-requirements/id-lifecycle.md`:
   - **Add**: a new item.
   - **Wording change**: same meaning, keep the ID.
   - **Meaning change**: withdraw the old ID, create a new one.
   - **Withdraw**, **split** or **merge**.
3. If you are not sure whether it is wording or meaning, **ask the user**. Do not guess.

## Step 3 · Find the impact

1. For each affected ID, run:

   ```bash
   python3 tools/reqcheck.py impact <ID>
   ```

2. For a new item, run `impact` on each item it will point to.
3. Use [reference/impact-map.md](reference/impact-map.md) to judge each result: ABOVE, BELOW, MENTIONED BY and OUTSIDE.
4. Also check the glossary: does the change use a term that is not in `docs/01-glossary/01-glossary.md`?

## Step 4 · Propose. Then stop.

Show the user one table. Do not edit any file yet.

| ID  | File | Change                                   | Reason             |
| --- | ---- | ---------------------------------------- | ------------------ |
| …   | …    | add / edit / withdraw / no change needed | one short sentence |

Below the table, list:

1. **Coverage after the change**: any problem, use case or actor that will lose its cover, and how you fix it.
2. **Outside the requirements folder**: tests, code, ADRs, experiment reports that mention the IDs. You only **list** these. You do not edit code or accepted ADRs.
3. **Vision or scope**: say so if the change adds or removes scope. Do not edit `docs/00-vision/00-vision.md` without approval.
4. **Open questions**: anything the user must decide.

Wait for the user to approve, change or reject.

## Step 5 · Apply

1. Make every approved edit, in all files, in one go.
2. Follow the writing rules of each file: fields in the right order, bullet lists, glossary words, links that point up.
3. Update the **Index** table of every file you changed. For the spec, update the area range.
4. For new IDs and withdrawn IDs, follow `docs/02-requirements/id-lifecycle.md` exactly.
5. Add new glossary terms if needed.

## Step 6 · Check

1. Run:

   ```bash
   python3 tools/reqcheck.py check
   ```

2. Fix every **ERROR**. Explain each **WARN** that you leave in place.
3. Re-read each changed item against the writing rules of its file. The script cannot check meaning.

## Step 7 · Log

Add an entry to `docs/05-journal/YYYY-MM-DD.md` (today's date). Create the file if it does not exist.

```markdown
## Requirements change: <short title>

- **Changed:** <IDs, with type: added / wording / meaning / withdrawn>
- **Why:** <one or two sentences, in the user's words if possible>
- **Impact:** <other IDs updated>
- **To check by hand:** <tests, code, ADRs listed in step 4, or "none">
```

## Finish

Tell the user in a few lines:

- what changed;
- the check result (errors and warnings);
- what is left for them to do by hand.
