# Specification

## Writing rules

Based on:
- ISO/IEC/IEEE 29148:2018 (characteristics of good requirements).
- EARS, Easy Approach to Requirements Syntax (Mavin et al., Rolls-Royce, 2009).
- Quality attribute scenarios (Bass, Clements, Kazman, *Software Architecture in Practice*, SEI).

**Meaning (ISO/IEC/IEEE 29148)**

Every requirement must be:

1. **Necessary**: if it is removed, something a use case or problem needs is missing.
2. **Singular**: it states one thing. No "and" joining two behaviours.
3. **Unambiguous**: it has only one meaning. Avoid words like *fast, easy, flexible, user-friendly, etc., and/or, some*.
4. **Verifiable**: it can be checked by test, analysis, demonstration or inspection.
5. **Implementation-free**: it says **what** the system does, not **how**. No class names, frameworks, databases or protocols. These go in ADRs.
6. **Traceable**: it points up to at least one use case (UC-xx) or problem (P-xx).
7. **Consistent**: it does not conflict with another requirement, and it uses the words from the [glossary](../01-glossary/01-glossary.md).

**Wording (EARS)**

8. Functional requirements use one of these patterns. "Shall" is used only here.
    - **Always:** The system shall `<response>`.
    - **Event:** When `<trigger>`, the system shall `<response>`.
    - **State:** While `<state>`, the system shall `<response>`.
    - **Unwanted:** If `<condition>`, then the system shall `<response>`.
    - **Option:** Where `<feature is included>`, the system shall `<response>`.
    - **Complex:** a mix of the above (e.g. While… when…).

**Quality requirements (quality attribute scenarios)**

9. Every NFR is written as six parts: **Source, Stimulus, Environment, Artifact, Response, Response measure**.
10. The response measure must be a number or a count.
11. A number marked **(draft)** is a first guess. It may change after the first real measurement. The reason for the change goes in the journal.

**Types and format**

12. Types:
    - **FR**: functional requirement. What the system does. Points to UC-xx.
    - **DR**: domain rule. A rule of the trading domain that must always hold. Points to P-xx.
    - **NFR**: quality requirement. How well the system does it. Points to P-xx and/or UC-xx.
    - **CON**: constraint. A fixed limit on the project.
13. IDs: `FR-<AREA>-01`, `DR-01`, `NFR-01`, `CON-01`. An ID never changes and is never reused. A removed requirement is marked **Withdrawn**, not deleted.
14. Each requirement is one `####` heading with its ID (areas use `###`), then these fields in this order:
    - **Statement**
    - **Why**
    - **Traces to**
    - **Verified by**: Test, Analysis, Demonstration or Inspection.
    - **Acceptance criteria**: added only when work on the requirement starts, written as Given / When / Then.
15. Use bullet lists. Do not put several ideas on one line.

**Links**

16. Chain: Actors → Problems → Use Cases → **Spec**.
17. Each requirement points **up** only. Code, tests and commits point to requirement IDs.
18. Coverage: every use case must be covered by at least one FR. Every problem must be covered by a use case, a DR or an NFR.

---

## Index

**Functional (FR)**

| Area | IDs |
|---|---|
| Market data (MD) | [FR-MD-01](#fr-md-01) – [FR-MD-06](#fr-md-06) |
| Charts (CH) | [FR-CH-01](#fr-ch-01) – [FR-CH-05](#fr-ch-05) |
| Strategies (ST) | [FR-ST-01](#fr-st-01) – [FR-ST-04](#fr-st-04) |
| Composite (CO) | [FR-CO-01](#fr-co-01) – [FR-CO-04](#fr-co-04) |
| Backtest (BT) | [FR-BT-01](#fr-bt-01) – [FR-BT-03](#fr-bt-03) |
| Evaluation (EV) | [FR-EV-01](#fr-ev-01) – [FR-EV-02](#fr-ev-02) |
| Walk-forward (WF) | [FR-WF-01](#fr-wf-01) – [FR-WF-03](#fr-wf-03) |
| Search (SE) | [FR-SE-01](#fr-se-01) – [FR-SE-05](#fr-se-05) |
| Leaderboard (LB) | [FR-LB-01](#fr-lb-01) – [FR-LB-04](#fr-lb-04) |
| Run control (RC) | [FR-RC-01](#fr-rc-01) – [FR-RC-03](#fr-rc-03) |
| Reproducibility (RP) | [FR-RP-01](#fr-rp-01) – [FR-RP-02](#fr-rp-02) |
| News (NW) | [FR-NW-01](#fr-nw-01) – [FR-NW-04](#fr-nw-04) |
| Extension (EX) | [FR-EX-01](#fr-ex-01) – [FR-EX-03](#fr-ex-03) |

**Domain rules (DR)**: [DR-01](#dr-01) – [DR-06](#dr-06)

**Quality (NFR)**: [NFR-01](#nfr-01) – [NFR-10](#nfr-10)

**Constraints (CON)**: [CON-01](#con-01) – [CON-03](#con-03)

---

## Functional requirements

### Market data

#### FR-MD-01

- **Statement:** When a test needs candles that are not stored, the system shall download only the missing candles for the chosen pair, timeframe and range.
- **Why:** Downloading the same data again wastes time and hits provider limits.
- **Traces to:** [UC-16](03-use-cases.md#uc-16)
- **Verified by:** Test.

#### FR-MD-02

- **Statement:** When candles are stored, the system shall check the range for missing candles.
- **Why:** Missing candles make backtest results wrong without any warning.
- **Traces to:** [UC-16](03-use-cases.md#uc-16), [UC-02](03-use-cases.md#uc-02)
- **Verified by:** Test.

#### FR-MD-03

- **Statement:** When a market data provider sends a new price, the system shall update every open chart that shows that pair.
- **Why:** The researcher needs to see the market as it moves.
- **Traces to:** [UC-01](03-use-cases.md#uc-01)
- **Verified by:** Demonstration.

#### FR-MD-04

- **Statement:** If the live connection to a provider drops, then the system shall try to reconnect, waiting longer between each try.
- **Why:** Connections drop often. Retrying too fast can get the system blocked by the provider.
- **Traces to:** [UC-15](03-use-cases.md#uc-15)
- **Verified by:** Test.

#### FR-MD-05

- **Statement:** When the live connection comes back, the system shall fetch the candles missed while it was down.
- **Why:** Without this, the stored data has a hidden hole.
- **Traces to:** [UC-15](03-use-cases.md#uc-15)
- **Verified by:** Test.

#### FR-MD-06

- **Statement:** While the live connection is down, the system shall show on each affected chart that its data is not live.
- **Why:** The researcher must not mistake old prices for live ones.
- **Traces to:** [UC-01](03-use-cases.md#uc-01), [UC-15](03-use-cases.md#uc-15)
- **Verified by:** Demonstration.

### Charts

#### FR-CH-01

- **Statement:** The system shall show up to 4 candle charts on one screen, each with its own timeframe.
- **Why:** Different timeframes show different parts of the picture.
- **Traces to:** [UC-01](03-use-cases.md#uc-01)
- **Verified by:** Demonstration.

#### FR-CH-02

- **Statement:** When the researcher changes the timeframe of one chart, the system shall reload only that chart.
- **Why:** Reloading everything is slow and loses the researcher's view.
- **Traces to:** [UC-01](03-use-cases.md#uc-01)
- **Verified by:** Test.

#### FR-CH-03

- **Statement:** When the researcher opens a result, the system shall draw the indicators used by its strategy on the chart.
- **Why:** The researcher must see what the strategy was looking at.
- **Traces to:** [UC-07](03-use-cases.md#uc-07)
- **Verified by:** Demonstration.

#### FR-CH-04

- **Statement:** When the researcher opens a result, the system shall mark every entry and exit on the chart.
- **Why:** A final number does not explain what the strategy did.
- **Traces to:** [UC-07](03-use-cases.md#uc-07)
- **Verified by:** Demonstration.

#### FR-CH-05

- **Statement:** When the researcher selects a trade in the trade list, the system shall highlight its entry and exit on the chart.
- **Why:** It links the table to the picture, so one trade can be studied.
- **Traces to:** [UC-07](03-use-cases.md#uc-07)
- **Verified by:** Demonstration.

### Strategies

#### FR-ST-01

- **Statement:** The system shall list all registered strategies with their parameters and allowed ranges.
- **Why:** The researcher must know what can be tested.
- **Traces to:** [UC-03](03-use-cases.md#uc-03), [UC-10](03-use-cases.md#uc-10)
- **Verified by:** Test.

#### FR-ST-02

- **Statement:** When a candle closes, each active strategy shall produce exactly one signal: BUY, SELL or HOLD.
- **Why:** One clear output per candle makes strategies easy to combine and compare.
- **Traces to:** [UC-02](03-use-cases.md#uc-02)
- **Verified by:** Test.

#### FR-ST-03

- **Statement:** If a parameter value is outside its allowed range, then the system shall reject it and say which range is allowed.
- **Why:** Bad parameters waste test time and give meaningless results.
- **Traces to:** [UC-02](03-use-cases.md#uc-02), [UC-03](03-use-cases.md#uc-03)
- **Verified by:** Test.

#### FR-ST-04

- **Statement:** When a strategy or its parameters are saved, the system shall create a new version and keep the old one unchanged.
- **Why:** Every result must point to the exact strategy that produced it.
- **Traces to:** [UC-08](03-use-cases.md#uc-08)
- **Verified by:** Test.

### Composite

#### FR-CO-01

- **Statement:** The system shall let the researcher combine two or more strategies into one composite strategy.
- **Why:** One strategy alone often fails when the market changes.
- **Traces to:** [UC-03](03-use-cases.md#uc-03)
- **Verified by:** Test.

#### FR-CO-02

- **Statement:** The system shall let the researcher choose the rule that turns the combined signals into one signal (e.g. majority vote, weighted score).
- **Why:** Strategies often disagree. The rule decides who wins.
- **Traces to:** [UC-03](03-use-cases.md#uc-03)
- **Verified by:** Test.

#### FR-CO-03

- **Statement:** The system shall accept a composite strategy anywhere a single strategy is accepted.
- **Why:** Backtest, search and charts must not need special cases for composites.
- **Traces to:** [UC-03](03-use-cases.md#uc-03), [UC-04](03-use-cases.md#uc-04)
- **Verified by:** Test.

#### FR-CO-04

- **Statement:** Where news sentiment is available, the system shall offer it as an input that a composite strategy can use.
- **Why:** It lets the researcher test whether news adds value.
- **Traces to:** [UC-03](03-use-cases.md#uc-03)
- **Verified by:** Test.

### Backtest

#### FR-BT-01

- **Statement:** When the researcher starts a backtest, the system shall replay the candles in time order and record every simulated trade.
- **Why:** This is how the system answers "what would have happened?".
- **Traces to:** [UC-02](03-use-cases.md#uc-02)
- **Verified by:** Test.

#### FR-BT-02

- **Statement:** The system shall record for each trade: entry time, entry price, exit time, exit price, fees paid and result.
- **Why:** Metrics, charts and checks are all built from this record.
- **Traces to:** [UC-02](03-use-cases.md#uc-02), [UC-07](03-use-cases.md#uc-07)
- **Verified by:** Test.

#### FR-BT-03

- **Statement:** The system shall let the researcher set the starting balance, fee rate and slippage for each backtest.
- **Why:** Results depend on these values. They must be visible, not hidden defaults.
- **Traces to:** [UC-02](03-use-cases.md#uc-02)
- **Verified by:** Test.

### Evaluation

#### FR-EV-01

- **Statement:** When a backtest ends, the system shall calculate total return, win rate, maximum drawdown and number of trades.
- **Why:** Profit alone hides risk.
- **Traces to:** [UC-02](03-use-cases.md#uc-02), [UC-06](03-use-cases.md#uc-06)
- **Verified by:** Test.

#### FR-EV-02

- **Statement:** When a backtest ends, the system shall calculate profit factor and Sharpe ratio.
- **Why:** These compare gains with losses and with risk.
- **Traces to:** [UC-06](03-use-cases.md#uc-06)
- **Verified by:** Test.

### Walk-forward

#### FR-WF-01

- **Statement:** The system shall let the researcher set the length of the tuning window and the test window.
- **Why:** Window sizes change the result. They must be a visible choice.
- **Traces to:** [UC-05](03-use-cases.md#uc-05)
- **Verified by:** Test.

#### FR-WF-02

- **Statement:** When a walk-forward test runs, the system shall choose parameters on each tuning window and test them only on the next test window.
- **Why:** This is the only way to judge parameters on data they have not seen.
- **Traces to:** [UC-05](03-use-cases.md#uc-05)
- **Verified by:** Test.

#### FR-WF-03

- **Statement:** When all windows are done, the system shall join the test windows into one result and calculate its metrics.
- **Why:** The joined result is the honest score of the strategy.
- **Traces to:** [UC-05](03-use-cases.md#uc-05)
- **Verified by:** Test.

### Search

#### FR-SE-01

- **Statement:** The system shall let the researcher define a search space: strategies, parameter ranges and combination rules.
- **Why:** The search must only try what the researcher allows.
- **Traces to:** [UC-04](03-use-cases.md#uc-04)
- **Verified by:** Test.

#### FR-SE-02

- **Statement:** The system shall provide a search method that picks candidates at random from the search space.
- **Why:** Random search is the simplest baseline. Smarter methods are compared against it.
- **Traces to:** [UC-04](03-use-cases.md#uc-04)
- **Verified by:** Test.

#### FR-SE-03

- **Statement:** The system shall let the researcher choose the search method for each run.
- **Why:** Different methods suit different search spaces.
- **Traces to:** [UC-04](03-use-cases.md#uc-04), [UC-11](03-use-cases.md#uc-11)
- **Verified by:** Test.

#### FR-SE-04

- **Statement:** If no stop condition is set, then the system shall not start the run.
- **Why:** A run with no end wastes time and computer power.
- **Traces to:** [UC-04](03-use-cases.md#uc-04)
- **Verified by:** Test.

#### FR-SE-05

- **Statement:** While a run is active, the system shall not test the same candidate twice.
- **Why:** Repeated tests waste time and give no new information.
- **Traces to:** [UC-04](03-use-cases.md#uc-04)
- **Verified by:** Test.

### Leaderboard

#### FR-LB-01

- **Statement:** When a candidate's score is higher than the lowest score in the top K, the system shall add it to the leaderboard.
- **Why:** The researcher only needs the best results, not every result.
- **Traces to:** [UC-06](03-use-cases.md#uc-06)
- **Verified by:** Test.

#### FR-LB-02

- **Statement:** The system shall let the researcher sort the leaderboard by any metric.
- **Why:** The best strategy depends on what the researcher cares about.
- **Traces to:** [UC-06](03-use-cases.md#uc-06)
- **Verified by:** Test.

#### FR-LB-03

- **Statement:** The system shall show the formula of the overall score, including the weight of each metric.
- **Why:** A score with a hidden formula cannot be trusted.
- **Traces to:** [UC-06](03-use-cases.md#uc-06)
- **Verified by:** Inspection.

#### FR-LB-04

- **Statement:** When the leaderboard changes, the system shall update every open leaderboard view without a page reload.
- **Why:** The researcher watches results arrive during a long search.
- **Traces to:** [UC-06](03-use-cases.md#uc-06), [UC-13](03-use-cases.md#uc-13)
- **Verified by:** Demonstration.

### Run control

#### FR-RC-01

- **Statement:** The system shall let the operator pause, resume and stop a running search.
- **Why:** The operator must be able to end a bad run without losing work.
- **Traces to:** [UC-14](03-use-cases.md#uc-14)
- **Verified by:** Test.

#### FR-RC-02

- **Statement:** While a search runs, the system shall show its state, candidates tested, candidates failed, time used and current best.
- **Why:** Without this, a long run is a black box.
- **Traces to:** [UC-13](03-use-cases.md#uc-13)
- **Verified by:** Demonstration.

#### FR-RC-03

- **Statement:** If one candidate fails, then the system shall record the error and continue with the next candidate.
- **Why:** One bad candidate must not end a long run.
- **Traces to:** [UC-04](03-use-cases.md#uc-04), [UC-13](03-use-cases.md#uc-13)
- **Verified by:** Test.

### Reproducibility

#### FR-RP-01

- **Statement:** The system shall link each result to its strategy version, parameters, data range, settings and random seed.
- **Why:** Without these, nobody can tell how a result was made.
- **Traces to:** [UC-08](03-use-cases.md#uc-08)
- **Verified by:** Inspection.

#### FR-RP-02

- **Statement:** When the researcher re-runs a past result, the system shall use the exact inputs linked to it and report whether the new result matches.
- **Why:** A result that cannot be repeated cannot be trusted.
- **Traces to:** [UC-08](03-use-cases.md#uc-08)
- **Verified by:** Test.

### News

#### FR-NW-01

- **Statement:** The system shall collect news items from every registered news source on a schedule.
- **Why:** News must be up to date to be useful.
- **Traces to:** [UC-09](03-use-cases.md#uc-09)
- **Verified by:** Test.

#### FR-NW-02

- **Statement:** The system shall store every news item in one common format: title, content, source, published time, collected time, related coins and link.
- **Why:** Later steps must not depend on where the news came from.
- **Traces to:** [UC-09](03-use-cases.md#uc-09), [UC-12](03-use-cases.md#uc-12)
- **Verified by:** Test.

#### FR-NW-03

- **Statement:** When a news item is stored, the system shall give it a sentiment label (positive, neutral or negative) and a score.
- **Why:** The researcher and strategies need to know if the news is good or bad.
- **Traces to:** [UC-09](03-use-cases.md#uc-09)
- **Verified by:** Test.

#### FR-NW-04

- **Statement:** The system shall show recent news for a chosen coin with the share of positive, neutral and negative items.
- **Why:** The researcher needs the overall mood, not only single articles.
- **Traces to:** [UC-09](03-use-cases.md#uc-09)
- **Verified by:** Demonstration.

### Extension

#### FR-EX-01

- **Statement:** When a new strategy is registered, the system shall make it available in backtests, composites, searches and charts.
- **Why:** Adding a strategy must not need changes in each feature.
- **Traces to:** [UC-10](03-use-cases.md#uc-10)
- **Verified by:** Test.

#### FR-EX-02

- **Statement:** When a new search method is registered, the system shall offer it as a choice when a search starts.
- **Why:** Search methods must be swappable.
- **Traces to:** [UC-11](03-use-cases.md#uc-11)
- **Verified by:** Test.

#### FR-EX-03

- **Statement:** When a new data source is registered, the system shall collect its data in the common internal format.
- **Why:** Screens and strategies must not depend on any one source.
- **Traces to:** [UC-12](03-use-cases.md#uc-12)
- **Verified by:** Test.

---

## Domain rules

#### DR-01

- **Statement:** A strategy decision at time *t* shall use only candles that closed at or before *t*.
- **Why:** Using future data gives results that are impossible in real life.
- **Traces to:** [P-05](02-problems.md#p-05)
- **Verified by:** Test. Adding candles after *t* must not change any signal at or before *t*.

#### DR-02

- **Statement:** Every simulated trade shall include fees and slippage.
- **Why:** Ignoring costs makes strategies that trade often look better than they are.
- **Traces to:** [P-06](02-problems.md#p-06)
- **Verified by:** Test.

#### DR-03

- **Statement:** The leaderboard shall rank strategies by out-of-sample (walk-forward) results only.
- **Why:** Ranking by in-sample results rewards luck.
- **Traces to:** [P-04](02-problems.md#p-04)
- **Verified by:** Test.

#### DR-04

- **Statement:** The same data, strategy version, settings and random seed shall always give the same trades and metrics.
- **Why:** A result that changes on each run cannot be trusted or compared.
- **Traces to:** [P-09](02-problems.md#p-09)
- **Verified by:** Test.

#### DR-05

- **Statement:** If the data for a test range has missing candles, then the system shall not run the test until the gap is filled or accepted by the researcher.
- **Why:** Hidden gaps make results wrong without any warning.
- **Traces to:** [P-17](02-problems.md#p-17)
- **Verified by:** Test.

#### DR-06

- **Statement:** A saved result shall never be changed or deleted by a later run.
- **Why:** Old results are the history that new results are compared with.
- **Traces to:** [P-09](02-problems.md#p-09)
- **Verified by:** Test.

---

## Quality requirements

#### NFR-01

**Modifiability: add a strategy**

- **Source:** Strategy developer.
- **Stimulus:** Adds a new strategy (e.g. MACD).
- **Environment:** Development time.
- **Artifact:** The code base.
- **Response:** The strategy works in backtests, composites, searches and charts.
- **Response measure:**
    - 0 changes to backtest, evaluation, search, leaderboard or screen code.
    - At most 2 files touched outside the new strategy's own files.
- **Traces to:** [P-11](02-problems.md#p-11), [UC-10](03-use-cases.md#uc-10)
- **Verified by:** Inspection of the change set.

#### NFR-02

**Modifiability: add a search method**

- **Source:** Strategy developer.
- **Stimulus:** Adds a new search method (e.g. a genetic algorithm).
- **Environment:** Development time.
- **Artifact:** The code base.
- **Response:** The method can be chosen for a run.
- **Response measure:**
    - 0 changes to backtest, evaluation or leaderboard code.
- **Traces to:** [P-12](02-problems.md#p-12), [UC-11](03-use-cases.md#uc-11)
- **Verified by:** Inspection of the change set.

#### NFR-03

**Modifiability: add a data source**

- **Source:** Strategy developer.
- **Stimulus:** Adds a new market data provider or news source.
- **Environment:** Development time.
- **Artifact:** The code base.
- **Response:** Data from the new source appears in charts or news.
- **Response measure:**
    - 0 changes to frontend code.
    - 0 changes to strategy code.
- **Traces to:** [P-13](02-problems.md#p-13), [UC-12](03-use-cases.md#uc-12)
- **Verified by:** Inspection of the change set.

#### NFR-04

**Performance: single backtest**

- **Source:** Researcher or search run.
- **Stimulus:** Runs one backtest of a single strategy.
- **Environment:** 1 year of 5-minute candles, on the reference machine (see CON-03), data already stored.
- **Artifact:** Backtest and evaluation.
- **Response:** The result and metrics are ready.
- **Response measure:** at most 500 ms (draft).
- **Traces to:** [P-01](02-problems.md#p-01), [P-16](02-problems.md#p-16)
- **Verified by:** Test (benchmark).

#### NFR-05

**Scalability: search throughput**

- **Source:** Search run.
- **Stimulus:** Tests 10,000 candidates.
- **Environment:** Normal load, on the reference machine.
- **Artifact:** Search and backtest.
- **Response:** All candidates are tested and ranked.
- **Response measure:**
    - Total time at most 30 minutes (draft).
    - Doubling the CPU cores gives at least 1.6× more candidates per minute (draft).
- **Traces to:** [P-16](02-problems.md#p-16)
- **Verified by:** Test (benchmark).

#### NFR-06

**Latency: live price to chart**

- **Source:** Market data provider.
- **Stimulus:** Sends a new price.
- **Environment:** Normal operation, up to 4 open charts.
- **Artifact:** Market data flow and charts.
- **Response:** The chart shows the new price.
- **Response measure:** within 1 second for 95% of updates (draft).
- **Traces to:** [P-08](02-problems.md#p-08), [UC-01](03-use-cases.md#uc-01)
- **Verified by:** Test (measurement).

#### NFR-07

**Reliability: lost connection**

- **Source:** Market data provider.
- **Stimulus:** The live connection drops.
- **Environment:** Normal operation. The provider comes back within 5 minutes.
- **Artifact:** Market data flow.
- **Response:** The system reconnects and fills the gap.
- **Response measure:**
    - Live data again within 30 seconds after the provider is back (draft).
    - 0 missing candles after recovery.
- **Traces to:** [P-17](02-problems.md#p-17), [UC-15](03-use-cases.md#uc-15)
- **Verified by:** Test (simulated disconnect).

#### NFR-08

**Fault isolation: side feature failure**

- **Source:** News source or sentiment step.
- **Stimulus:** Fails or stops responding.
- **Environment:** Normal operation, a search is running.
- **Artifact:** Charts, backtest, search, leaderboard.
- **Response:** These features keep working.
- **Response measure:**
    - 0 failed candidates caused by the news failure.
    - Charts keep updating.
- **Traces to:** [P-18](02-problems.md#p-18)
- **Verified by:** Test (fault injection).

#### NFR-09

**Observability: run status**

- **Source:** Lab operator.
- **Stimulus:** Opens the run status view.
- **Environment:** A search is running.
- **Artifact:** Run status.
- **Response:** The view shows the current values.
- **Response measure:** values are at most 5 seconds old (draft).
- **Traces to:** [P-14](02-problems.md#p-14), [UC-13](03-use-cases.md#uc-13)
- **Verified by:** Demonstration.

#### NFR-10

**Control: stop a run**

- **Source:** Lab operator.
- **Stimulus:** Asks to pause or stop a run.
- **Environment:** A search is running.
- **Artifact:** Search run.
- **Response:** The run pauses or stops.
- **Response measure:**
    - Takes effect within 10 seconds (draft).
    - 0 finished results lost.
- **Traces to:** [P-15](02-problems.md#p-15), [UC-14](03-use-cases.md#uc-14)
- **Verified by:** Test.

---

## Constraints

#### CON-01

- **Statement:** The backend shall be written in Java.
- **Why:** The project's learning goal. The choice is checked against measurements in an ADR.
- **Traces to:** Project context.
- **Verified by:** Inspection.

#### CON-02

- **Statement:** The system shall never send real orders or move real money.
- **Why:** The project is a simulation. Real trading brings legal and money risk.
- **Traces to:** [Vision](../00-vision/00-vision.md), out of scope.
- **Verified by:** Inspection.

#### CON-03

- **Statement:** All performance targets shall be measured on one reference machine, described in the experiments folder.
- **Why:** Numbers from different machines cannot be compared.
- **Traces to:** [NFR-04](#nfr-04), [NFR-05](#nfr-05), [NFR-06](#nfr-06)
- **Verified by:** Inspection.
