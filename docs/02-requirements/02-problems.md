# Problems

## Writing rules

Based on: the RUP Vision problem statement ("The problem of… affects… the impact of which is… a successful solution would…"), as used in Craig Larman, *Applying UML and Patterns*.

**Meaning**

1. A problem describes **pain that exists today**, without this system.
2. A problem never names a solution or a technology. Write "results arrive too late", not "we need a job queue".
3. One entry = one problem. If a sentence has "and" joining two pains, split it.
4. The **Impact** must be something you can observe: lost time, wrong decisions, missing data.
5. **A good solution would** describes the outcome, not the mechanism. Write "the user sees the state at any time", not "add a dashboard with WebSocket".
6. Every problem belongs to at least one actor (A-xx).
7. Every problem must later be covered by at least one use case (UC-xx) or one requirement (NFR / DR) in the spec. A problem with no cover is a gap.

**Format**

8. IDs: `P-01`, `P-02`… An ID never changes and is never reused. A removed problem is marked **Withdrawn**, not deleted.
9. Problems are grouped by their main actor.
10. Each problem is one `###` heading with its ID, a bold name, then exactly four fields: **Problem**, **Affects**, **Impact**, **A good solution would**.
11. Use bullet lists. Do not put several ideas on one line.

**Links**

12. Chain: Actors → **Problems** → Use Cases → Spec.
13. Each problem points **up** to its actor(s) in **Affects**. It does not list links down.

---

## Index

| ID | Name | Affects |
|---|---|---|
| [P-01](#p-01) | Testing one idea by hand is slow | A-01 |
| [P-02](#p-02) | One strategy alone fails when the market changes | A-01 |
| [P-03](#p-03) | Too many combinations to try by hand | A-01 |
| [P-04](#p-04) | A good result is often just luck | A-01 |
| [P-05](#p-05) | A test can use future data | A-01 |
| [P-06](#p-06) | Profit alone hides risk and cost | A-01 |
| [P-07](#p-07) | A number alone does not explain a strategy | A-01 |
| [P-08](#p-08) | One timeframe gives an incomplete view | A-01 |
| [P-09](#p-09) | Old results cannot be repeated | A-01 |
| [P-10](#p-10) | Price data ignores news | A-01 |
| [P-11](#p-11) | A new strategy touches many parts | A-02 |
| [P-12](#p-12) | A new search method forces a rewrite | A-02 |
| [P-13](#p-13) | Each data source has its own format | A-02 |
| [P-14](#p-14) | A long run is a black box | A-03 |
| [P-15](#p-15) | A run does not stop by itself | A-03 |
| [P-16](#p-16) | Many tests take too long | A-03 |
| [P-17](#p-17) | The live data connection drops | A-03 |
| [P-18](#p-18) | One broken part stops everything | A-03 |

---

## Strategy Researcher (A-01)

### P-01

**Testing one idea by hand is slow**

- **Problem:** To test one strategy idea, a person must collect old prices, write a script and calculate the results by hand.
- **Affects:** [A-01](01-actors.md#a-01)
- **Impact:**
    - One test takes hours.
    - Most ideas are never tested.
- **A good solution would:** let the researcher test an idea in minutes, without writing code.

### P-02

**One strategy alone fails when the market changes**

- **Problem:** A strategy that works in one market mood often fails in another. Example: a trend strategy loses money when the price moves sideways.
- **Affects:** [A-01](01-actors.md#a-01)
- **Impact:**
    - Results change a lot from one period to another.
    - The researcher has no simple way to mix strategies when they disagree.
- **A good solution would:** let the researcher combine strategies and decide how disagreements are settled.

### P-03

**Too many combinations to try by hand**

- **Problem:** A few strategies with a few settings each already give hundreds of combinations.
- **Affects:** [A-01](01-actors.md#a-01)
- **Impact:**
    - Only the combinations the researcher thinks of are tested.
    - Better combinations are never found.
- **A good solution would:** try many combinations automatically and keep the best ones.

### P-04

**A good result is often just luck**

- **Problem:** When many combinations are tried on the same old data, some look great only by chance.
- **Affects:** [A-01](01-actors.md#a-01)
- **Impact:**
    - The researcher trusts a strategy that fails on new data.
    - This is the biggest risk in this field.
- **A good solution would:** judge every strategy on data it has never seen.

### P-05

**A test can use future data**

- **Problem:** It is easy to make a decision with information that was not known yet. Example: using a candle's close price before the candle has closed.
- **Affects:** [A-01](01-actors.md#a-01)
- **Impact:**
    - Results look great but are impossible in real life.
    - The bug is silent. Nothing crashes.
- **A good solution would:** make sure a decision can only use information that existed at that time.

### P-06

**Profit alone hides risk and cost**

- **Problem:** Two strategies with similar profit can carry very different risk. Results also often ignore trading fees.
- **Affects:** [A-01](01-actors.md#a-01)
- **Impact:**
    - The researcher picks a strategy that once lost almost half its money.
    - A strategy that trades very often looks good before fees and loses after fees.
- **A good solution would:** show risk and cost next to profit, for every strategy.

### P-07

**A number alone does not explain a strategy**

- **Problem:** A result like "+18%" does not show when the strategy bought, when it sold, or why.
- **Affects:** [A-01](01-actors.md#a-01)
- **Impact:**
    - The researcher cannot judge if the logic makes sense.
    - Bugs in a strategy stay hidden.
- **A good solution would:** let the researcher see every trade on the price chart.

### P-08

**One timeframe gives an incomplete view**

- **Problem:** A short timeframe can show the price going up while a long timeframe shows it going down.
- **Affects:** [A-01](01-actors.md#a-01)
- **Impact:**
    - The researcher misses context.
    - Switching between charts one by one is slow.
- **A good solution would:** show several timeframes side by side, with live prices.

### P-09

**Old results cannot be repeated**

- **Problem:** After a strategy's settings change, nobody knows which version produced an old result.
- **Affects:** [A-01](01-actors.md#a-01)
- **Impact:**
    - Old and new results cannot be compared fairly.
    - The ranking history cannot be trusted.
- **A good solution would:** let anyone run an old test again and get exactly the same result.

### P-10

**Price data ignores news**

- **Problem:** News (a hack, a new law) can move prices in minutes. Strategies based only on prices do not see it.
- **Affects:** [A-01](01-actors.md#a-01)
- **Impact:**
    - The researcher cannot test whether news adds value to a strategy.
- **A good solution would:** collect news, tell if it is good or bad, and let strategies use it.

## Strategy Developer (A-02)

### P-11

**A new strategy touches many parts**

- **Problem:** To add a new strategy (e.g. MACD), the developer must change the engine, the screens, the storage and the search code.
- **Affects:** [A-02](01-actors.md#a-02)
- **Impact:**
    - Each new strategy is slow to add.
    - Old features break.
- **A good solution would:** let the developer add a strategy without changing existing parts.

### P-12

**A new search method forces a rewrite**

- **Problem:** Moving from one search method to a smarter one also means changing the testing code.
- **Affects:** [A-02](01-actors.md#a-02)
- **Impact:**
    - The developer avoids trying better search methods.
- **A good solution would:** let search methods be swapped without touching testing, scoring or ranking.

### P-13

**Each data source has its own format**

- **Problem:** Every price provider and every news source sends data in a different shape.
- **Affects:** [A-02](01-actors.md#a-02)
- **Impact:**
    - Adding a source means changing code far away from it, even the screens.
- **A good solution would:** let the developer add a source without changing the rest of the system.

## Lab Operator (A-03)

### P-14

**A long run is a black box**

- **Problem:** A search can run for hours with no information about its progress.
- **Affects:** [A-03](01-actors.md#a-03)
- **Impact:**
    - The operator cannot tell if the run is working, stuck or broken.
- **A good solution would:** show the state of a run at any time.

### P-15

**A run does not stop by itself**

- **Problem:** A search with no clear end keeps going after it stops finding better results.
- **Affects:** [A-03](01-actors.md#a-03)
- **Impact:**
    - Time and computer power are wasted.
    - The operator must kill the run by hand and may lose results.
- **A good solution would:** end every run by a clear rule, and let the operator pause or stop it safely.

### P-16

**Many tests take too long**

- **Problem:** If one test takes 2 seconds, 10,000 tests take more than 5 hours.
- **Affects:** [A-03](01-actors.md#a-03), [A-01](01-actors.md#a-01)
- **Impact:**
    - Search results arrive too late to be useful.
- **A good solution would:** finish many tests in a short time, and get faster when more computer power is added.

### P-17

**The live data connection drops**

- **Problem:** The live connection to a data provider can close at any time, without warning.
- **Affects:** [A-03](01-actors.md#a-03), [A-04](01-actors.md#a-04)
- **Impact:**
    - Charts freeze.
    - Candles go missing, and missing candles make results wrong.
- **A good solution would:** reconnect by itself and fill the missing data.

### P-18

**One broken part stops everything**

- **Problem:** A failure in a side feature (e.g. a news source) can bring down the whole app.
- **Affects:** [A-03](01-actors.md#a-03), [A-05](01-actors.md#a-05)
- **Impact:**
    - A small problem blocks the main work.
- **A good solution would:** keep the main features working when a side feature fails.
