---
name: req-check
description: Review docs/02-requirements against its writing rules. Runs the mechanical check (links, IDs, index tables, coverage) and then reviews meaning (no solutions in problems, EARS wording, one behaviour per requirement, measurable NFRs, glossary words, no hard-fit product names). Reports only; does not edit.
when_to_use: Use after any change to the requirements, before a commit or pull request, or when the user asks to check, review, lint or validate the requirements.
argument-hint: "[optional: file name or ID to focus on]"
allowed-tools: Read Grep Glob Bash(python3 tools/reqcheck.py *) Bash(python tools/reqcheck.py *)
context: fork
agent: req-reviewer
background: false
---

# Check the requirements

Focus (optional): $ARGUMENTS

## Context you need

This skill runs in a forked context. You cannot see the conversation that started it, so everything you need is below.

1. The repository is a documentation project. Requirements live in `docs/02-requirements/`.
2. There are four files, and they form a chain: `01-actors.md` -> `02-problems.md` -> `03-use-cases.md` -> `04-spec.md`. Links point **up** only.
3. Each file starts with a **Writing rules** section. Those rules are the only rules you judge by.
4. `tools/reqcheck.py` is the mechanical checker. Run every command from the repository root.
5. Your job is to **report**. You do not edit any file.

## Mechanical check result

```!
cd "${CLAUDE_PROJECT_DIR}" && "$(command -v python3 || command -v python)" tools/reqcheck.py check; true
```

If the block above is empty or shows an error running the script, run the check yourself from the repository root: `python tools/reqcheck.py check`. Use `python3` if `python` is not found.

Those two commands, and `python tools/reqcheck.py impact <ID>`, are the only Bash commands you may run. A guard blocks anything else, including pipes, redirects and `&&`. Do not copy the command from the block above into a Bash call.

## Your job

The script checks structure. You check **meaning**. Do not edit any file.

### Step 1 · Read the rules

Read the **Writing rules** section at the top of each file in `docs/02-requirements/`. These are the only rules. Do not invent new ones.

If a focus is given, review only that file or ID, plus the items directly above and below it.

### Step 2 · Review each item

For each item, check the rules of its file. The checks the script **cannot** do are the most important:

1. **Actors**: Is it a role, not a person? Is an external system named by its role, with product names only as examples?
2. **Problems**:
   - Does it describe pain that exists today?
   - Does it name a solution or a technology? (not allowed)
   - Is it one problem, or two joined by "and"?
   - Is the impact observable?
   - Does "A good solution would" describe an outcome, not a mechanism?
3. **Use cases**:
   - Is the name a goal, written as an active verb phrase?
   - Is the system a black box (no classes, frameworks, databases, screen controls)?
   - Do steps show intent, not UI clicks?
   - Is the main scenario 3 to 9 steps, with no "if"?
   - Does each extension start from a real step number?
4. **Spec**:
   - Is the statement **necessary**: does a use case or problem really need it?
   - Is it **singular**: one behaviour only?
   - Is it **unambiguous**: one meaning only?
   - Is it **verifiable**: could you write a test or a measurement for it?
   - Is it **implementation-free**: no class, framework, database or protocol names?
   - Does an FR follow an EARS pattern that fits its meaning (event → When, state → While, failure → If…then)?
   - Does an NFR have all six parts, with a number in the response measure?
   - Do two requirements conflict?
5. **All files**: Are the terms in `docs/01-glossary/01-glossary.md`? Is the English short and simple (about IELTS 6.5)?

### Step 3 · Look at the whole set

1. **Complete**: Is there a problem that no item really solves, even if a link exists?
2. **Consistent**: Is the same thing called by two different names?
3. **Drift**: Does a use case still match the requirements that trace to it?

## Report

Start with one line: `Mechanical: X errors, Y warnings. Meaning: Z findings.`

Then one table, most serious first:

| Severity            | ID   | Rule            | Finding                              | Suggested fix                |
| ------------------- | ---- | --------------- | ------------------------------------ | ---------------------------- |
| High / Medium / Low | P-07 | problems rule 2 | names a solution ("add a dashboard") | describe the outcome instead |

- **High**: wrong meaning, broken chain, untestable requirement, conflict.
- **Medium**: rule broken but meaning is clear.
- **Low**: wording or style.

End with: "To fix these, use `/req-change`." Do not fix them yourself.
