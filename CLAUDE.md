@AGENTS.md

## Claude skills

- `/req-update` — a full requirements change, with review. Chains `req-change` then `req-check`.
- `/req-change` — the requirements change on its own, without the review.
- `/req-check` — review the requirements and report. Never edits.
