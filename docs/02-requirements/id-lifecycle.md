# ID lifecycle

How IDs are created, changed and retired in `docs/02-requirements/`.
These rules apply to every AI and every human that edits the files.

## Why this matters

Code, tests, commits, ADRs, journal entries and saved results all point to IDs.
If an ID changes meaning, all of those links silently point to the wrong thing.

## 1. Creating a new item

1. Find the largest number already used for that prefix, **including withdrawn items**.
2. The new ID is that number + 1.
    - Example: `FR-SE-01` … `FR-SE-05` exist, and `FR-SE-03` is withdrawn. The new ID is `FR-SE-06`.
3. Never fill a gap. Never reuse a number.
4. Add the item in two places:
    - the body, in the right group;
    - the Index table (for spec: update the range of its area).

## 2. Changing an item: wording or meaning?

Ask one question: **would a test written for the old version still be a correct test for the new version?**

| Answer | Type of change | What to do |
|---|---|---|
| Yes | **Wording change**. Clearer words, a typo, a better example. | Edit in place. Keep the ID. |
| No | **Meaning change**. Different behaviour, different scope, different actor, different number. | Withdraw the old ID. Create a new ID. |

Special case: a number marked **(draft)** in an NFR may change in place after a real measurement. This is allowed because the rule in the spec says so. The reason must go in the journal.

When unsure, treat it as a **meaning change**.

## 3. Withdrawing an item

1. Do **not** delete the heading or the item.
2. Add this field as the first field under the bold name:

    ```markdown
    - **Status:** Withdrawn (YYYY-MM-DD). Replaced by [NEW-ID](#new-id). Reason: <one sentence>.
    ```

    - If nothing replaces it, write `Replaced by none.`
3. Keep the other fields as they were. They are history.
4. In the Index table, strike the name: `~~Old name~~ (withdrawn)`.
5. Every **active** item that pointed to the old ID must now point to the new ID, or stop pointing to it.
6. Run the check. Withdrawing can leave a gap in coverage (a problem with no use case, a use case with no FR). Fix the gap in the same change.

## 4. Splitting and merging

- **Split** (one item becomes two): withdraw the old ID, create two new IDs, and write `Replaced by A, B`.
- **Merge** (two items become one): withdraw both old IDs, create one new ID, and write `Replaced by X` in both.
