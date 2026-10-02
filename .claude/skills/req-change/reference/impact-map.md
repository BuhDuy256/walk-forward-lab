# Impact map

How to read the result of the impact step, when an item in `docs/02-requirements/` changes.

The procedure, the chain and the `reqcheck.py impact` command are in
[docs/02-requirements/AGENTS.md](../../../../docs/02-requirements/AGENTS.md). This file is
only the tables that say what each result means.

## Inside the chain

| You change…                 | Look ABOVE (does it still fit?)                                                  | Look BELOW (does it still hold?)                                                                                      |
| --------------------------- | -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Actor (A)**               | `docs/00-vision/00-vision.md`: is the actor in scope?                                           | Problems with this actor in **Affects**. Use cases with this actor as primary or supporting actor.                    |
| **Problem (P)**             | The actor(s) in **Affects**.                                                     | Use cases that list it in **Solves**. DRs and NFRs that list it in **Traces to**. Then the FRs below those use cases. |
| **Use case (UC)**           | The problems in **Solves**. The actors.                                          | FRs and NFRs that list it in **Traces to**. Other use cases that mention it (e.g. "used by", "continue with").        |
| **FR**                      | The use case(s) in **Traces to**. Does each use case still have at least one FR? | Tests, code and ADRs that use this ID.                                                                                |
| **DR / NFR**                | The problem(s) and use case(s) in **Traces to**.                                 | Tests, benchmarks (`bench/`), experiment reports (`docs/06-experiments/`), ADRs.                                      |
| **CON**                     | `docs/00-vision/00-vision.md`, and what it traces to.                                           | Every ADR. A constraint can make a past decision invalid.                                                             |
| **Writing rules** of a file | —                                                                                | **Every item in that file.** Run `req-check` on the whole folder.                                                     |

## Outside the chain

| Place                             | What to look for                                       | What to do                                                              |
| --------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| `docs/01-glossary/01-glossary.md` | A new or changed term.                                 | Add or update the term. Requirements must use glossary words.           |
| `docs/00-vision/00-vision.md`     | A change in scope (new feature, removed feature).      | Point it out to the user. Do not edit the vision without approval.      |
| `docs/03-adr/`                    | ADRs that mention the ID.                              | List them. The decision may need a new ADR. Never edit an accepted ADR. |
| `docs/05-journal/`                | —                                                      | Add a line for this change (format in `docs/02-requirements/AGENTS.md`). |
| `docs/06-experiments/`            | Reports measured against an NFR number.                | List them. Old numbers stay as history.                                 |
| Tests and code                    | The ID, with `-` or `_` (e.g. `FR-BT-02`, `FR_BT_02`). | List them. Do not edit code in a requirements change. The user decides. |

## Questions to ask for each item found

1. Is it still **true** after the change?
2. Does it still **cover** what it covered before?
3. Does it now point to something **withdrawn**?
4. Does its **wording** still match the glossary and the writing rules?

If the answer to any of these is "no", the item goes into the proposed change list.
