---
paths:
  - "docs/02-requirements/**"
---

# Requirements, in Claude Code

The workflow, the ID rules and the checker are in `AGENTS.md`. Follow those. This file only says which command to use.

1. For a **full change with review**, use `/req-update`. It runs the change, then the review in a fresh context, and repeats the fix while High findings remain (at most twice).
2. For a **review only**, use `/req-check`. It reports problems and never edits.
3. For the **change on its own**, without the review, use `/req-change`.

Do not edit a file under `docs/02-requirements/` by hand when one of these commands fits. They carry the impact analysis and the approval stop.
