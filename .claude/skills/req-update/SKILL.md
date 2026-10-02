---
name: req-update
description: Run a full requirements change end to end. It chains the req-change skill (edit with impact analysis) and the req-check skill (review in a fresh context), and repeats the fix at most twice while High findings remain. Manual only.
argument-hint: "[the change you want, e.g. withdraw UC-05 and move its FRs to UC-04]"
disable-model-invocation: true
allowed-tools: Skill
---

# Update the requirements, then have the work reviewed

Requested change: $ARGUMENTS

This skill is an **orchestrator**. It owns the order of the steps and nothing else.

## Hard rules

1. You do **not** edit any file in this skill. Only the sub-skills edit.
2. You do **not** do a sub-skill's work inline. If a sub-skill cannot be invoked, say which one and why, then **stop**.
3. You invoke each sub-skill with the **Skill** tool, by its name: `req-change` and `req-check`.
4. You keep the approval stop inside `req-change`. Never skip it, never answer it for the user.

## Step 1 · Make the change

1. Invoke the `req-change` skill with the requested change above as its argument.
2. `req-change` will show an impact table and then **stop for approval**. Let the user answer.
3. If the user rejects the change, stop here and say so.
4. When the change is applied, note the IDs it touched. You need them in Step 2.

## Step 2 · Review the change

1. Invoke the `req-check` skill. As its argument, give:
   - the IDs that changed, and
   - the items directly above and below them in the chain.
2. `req-check` runs in a fresh context, so it does not grade work it just did. It cannot see this conversation, so put the IDs in the argument. Do not rely on it guessing the focus.
3. Read the report it returns. Sort the findings by severity: High, Medium, Low.

## Step 3 · Fix the High findings

Repeat this at most **2 times**:

1. If the report has no **High** finding, go to Step 4.
2. Invoke `req-change` again. Give it **only the High findings** as its argument, nothing else.
3. Let it stop for approval again.
4. Invoke `req-check` again on the same IDs.

After the second round, stop even if High findings remain. Do not start a third round.

## Step 4 · Summary

End with a short summary, in this order:

1. **IDs changed** — each one, with the kind of change (added, wording, meaning, withdrawn).
2. **Mechanical check** — the error and warning count from the last `reqcheck` run.
3. **Review findings left** — every Medium and Low finding, and any High finding still open after 2 rounds. Say plainly that a High finding is still open, if it is.
4. **Work left by hand** — tests, code, ADRs and experiment reports that mention the changed IDs. `req-change` lists these. You only pass the list on. You do not edit them.
