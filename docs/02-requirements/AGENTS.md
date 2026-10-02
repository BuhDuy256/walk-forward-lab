# Requirements

The four files in this folder form a chain: **Actors → Problems → Use cases → Spec**.

1. `01-actors.md` (Actors)
2. `02-problems.md` (Problems)
3. `03-use-cases.md` (Use cases)
4. `04-spec.md` (Spec)

Links point **up** only, so an item does not list what depends on it. Changing one item can break items you cannot see from it.

- **How to write an item:** the **Writing rules** section at the top of each file above. Those rules are the only rules for that file. Read them before you change the file, and do not invent new rules.
- **IDs:** never delete, never renumber. Withdraw instead. A change of meaning gets a new ID; a change of wording keeps it. Full rules, with the test for wording against meaning: [id-lifecycle.md](id-lifecycle.md).
- **The checker:** `tools/reqcheck.py`. Its docstring says what it checks and what it cannot check.

## How to change a requirement

Never edit one item on its own. Follow these six steps in order. Run every command from the repository root; use `python3` if `python` is not found.

1. **Impact** — find every item above and below the one you are changing, and every ID mentioned outside this folder (code, tests, ADRs, experiment reports):

   ```bash
   python tools/reqcheck.py impact <ID>
   ```

2. **Propose** — show one table: ID, file, the change, and the reason. Add what loses its coverage, what sits outside this folder, and any open question. Do not edit a file yet.
3. **Approve** — wait for the person to approve, change or reject the proposal. Do not skip this.
4. **Apply** — make every approved edit, in all files, in one go. Update the **Index** table of every file you changed. Keep the fields in the order the Writing rules give.
5. **Check** — run the mechanical checker. It must show 0 errors:

   ```bash
   python tools/reqcheck.py check
   ```

   Fix every ERROR. Explain every WARN you leave in place. The checker cannot check meaning, so re-read each changed item against the Writing rules of its file.
6. **Journal** — add an entry to `docs/05-journal/YYYY-MM-DD.md` for today. Create the file if it does not exist:

   ```markdown
   ## Requirements change: <short title>

   - **Changed:** <IDs, with type: added / wording / meaning / withdrawn>
   - **Why:** <one or two sentences, in the person's words if possible>
   - **Impact:** <other IDs updated>
   - **To check by hand:** <tests, code, ADRs, or "none">
   ```
