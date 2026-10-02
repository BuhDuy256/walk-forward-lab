---
name: req-check
description: Review docs/02-requirements against its writing rules. Runs the mechanical check (links, IDs, index tables, coverage) and then reviews meaning, which the checker cannot do. Reports only; does not edit.
when_to_use: Use after any change to the requirements, before a commit or pull request, or when the user asks to check, review, lint or validate the requirements.
argument-hint: "[optional: file name or ID to focus on]"
allowed-tools: Read Grep Glob Bash(python3 tools/reqcheck.py *) Bash(python tools/reqcheck.py *)
context: fork
agent: req-reviewer
background: false
---

# Check the requirements

Focus (optional): $ARGUMENTS

This skill runs in a forked context, as the `req-reviewer` agent. You cannot see the conversation that started it. Your agent definition says which files to read, what you may run, and how to report. Follow it. This file only adds the run.

## Mechanical check result

```!
cd "${CLAUDE_PROJECT_DIR}" && "$(command -v python3 || command -v python)" tools/reqcheck.py check; true
```

If the block above is empty or shows an error running the script, run the check yourself from the repository root: `python tools/reqcheck.py check`. Use `python3` if `python` is not found. Do not copy the command from the block above into a Bash call.

## Your job

The script checks structure. You check **meaning**: everything in the Writing rules that no script can test.

### Step 1 · Review each item

Go file by file. For each item, work through the Writing rules of its own file, in the order they are written there, and judge the item against each rule. If a focus is given, review only that file or ID, plus the items directly above and below it in the chain.

Give most weight to the rules the script cannot test at all: whether an item describes what the rule says it should describe, whether it holds one thing and not two, whether it could be verified, and whether it names a solution, a technology or a product where the rules forbid it.

### Step 2 · Look at the whole set

1. **Complete**: Is there a problem that no item really solves, even if a link exists?
2. **Consistent**: Is the same thing called by two different names?
3. **Drift**: Does a use case still match the requirements that trace to it?
4. **Conflict**: Do two items contradict each other?

## Report

Start with one line, from the block above and your findings:

`Mechanical: X errors, Y warnings. Meaning: Z findings.`

Then the finding table your agent definition gives. End with: "To fix these, use `/req-change`." Do not fix anything yourself.
