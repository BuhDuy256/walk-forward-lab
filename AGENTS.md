# walk-forward-lab

A lab to build, combine and backtest crypto trading strategies, with walk-forward testing to check if a result is real.

## Where the documentation lives

- `docs/00-vision/00-vision.md` — start here. What the system is for, and what is out of scope.
- `docs/01-glossary/01-glossary.md` — the words. Use these words in every document.
- `docs/02-requirements/` — the requirements chain, in four files:
  1. `01-actors.md` (Actors)
  2. `02-problems.md` (Problems)
  3. `03-use-cases.md` (Use cases)
  4. `04-spec.md` (Spec)
- `docs/03-adr/` — architecture decisions. `docs/04-architecture/` — design. `docs/05-journal/` — a log, one file per day.
- `docs/06-experiments/` — experiment reports.

Each requirement file starts with a **Writing rules** section. Those rules are the only rules for that file. Read them before you change the file, and do not invent new rules.

## The requirements chain

The four files form a chain: Actors → Problems → Use cases → Spec. Links point **up** only. So changing one item can break items you cannot see from it.

## How to change a requirement

Never edit one item on its own. Follow these six steps in order.

1. **Impact** — find every item above and below the one you are changing, and every ID mentioned outside `docs/02-requirements/` (code, tests, ADRs, experiment reports):

   ```bash
   python tools/reqcheck.py impact <ID>
   ```

2. **Propose** — show one table: ID, file, the change, and the reason. Add what loses its coverage, what sits outside the requirements folder, and any open question. Do not edit a file yet.
3. **Approve** — wait for the person to approve, change or reject the proposal. Do not skip this.
4. **Apply** — make every approved edit, in all files, in one go. Update the **Index** table of every file you changed. Keep the fields in the order the Writing rules give.
5. **Check** — run the mechanical checker. It must show 0 errors:

   ```bash
   python tools/reqcheck.py check
   ```

   Use `python3` if `python` is not found. Fix every ERROR. Explain every WARN you leave in place.
6. **Journal** — add an entry to `docs/05-journal/YYYY-MM-DD.md` for today. Create the file if it does not exist. Record: what changed (IDs and the kind of change), why, the other IDs you updated, and what is left to check by hand.

## ID rules

- Never delete an ID. Never renumber an ID. Withdraw it instead.
- A change of **meaning** gets a new ID, and the old one is withdrawn. A change of **wording** keeps its ID.
- The full rules, with the test for wording against meaning, are in `docs/02-requirements/id-lifecycle.md`.

## What the checker does and does not do

`tools/reqcheck.py` checks structure: unique IDs, no gaps, required fields, links that resolve, index tables, coverage. It cannot check meaning. A human or an agent must still read each changed item against the Writing rules of its file.
