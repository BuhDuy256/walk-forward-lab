# Use Cases

## Writing rules

Based on: Alistair Cockburn, *Writing Effective Use Cases* (fully dressed template, goal levels, step guidelines).

**Meaning**

1. A use case describes how an actor uses the system to reach **one goal**.
2. The name is the goal, written as a short **active verb phrase**. Example: "Run a backtest", not "Backtest module".
3. The system is a **black box**. Describe what it does, never how it is built. No class names, no frameworks, no databases.
4. Steps show the actor's **intent**, not screen details. Write "The researcher chooses a date range", not "The researcher clicks the calendar icon".
5. Each step is one simple sentence: **who** does **what**. Either the actor or the system is the subject.
6. The main success scenario has **3 to 9 steps** and contains no "if". Every "if" goes into **Extensions**.
7. Each extension starts from a step: `2a. <condition>:` then the steps to handle it.
8. Every use case has a goal level:
    - **Summary**: a big goal made of several use cases.
    - **User goal**: one goal done in one sitting. Most use cases are here.
    - **Subfunction**: a part that is reused by other use cases.
9. **Success guarantee** = what is true when the goal is reached. **Minimal guarantee** = what is still true when it fails.
10. Use the words from the [glossary](../01-glossary/01-glossary.md). Do not invent new terms here.

**Format**

11. IDs: `UC-01`, `UC-02`… An ID never changes and is never reused. A removed use case is marked **Withdrawn**, not deleted.
12. Each use case is one `###` heading with its ID, a bold name, then these fields in this order: **Level, Primary actor, Supporting actors, Solves, Trigger, Preconditions, Success guarantee, Minimal guarantee, Main success scenario, Extensions**.
13. Use numbered lists for steps. Use bullet lists for everything else.

**Links**

14. Chain: Actors → Problems → **Use Cases** → Spec.
15. Each use case points **up**: to its actors (A-xx) and to the problems it solves (P-xx).
16. Every use case must solve at least one problem.

---

## Index

| ID | Name | Primary actor | Solves |
|---|---|---|---|
| [UC-01](#uc-01) | View live market charts | A-01 | P-08 |
| [UC-02](#uc-02) | Run a backtest | A-01 | P-01, P-05, P-06 |
| [UC-03](#uc-03) | Build a composite strategy | A-01 | P-02, P-10 |
| [UC-04](#uc-04) | Run a strategy search | A-01 | P-03, P-15 |
| [UC-05](#uc-05) | Run a walk-forward test | A-01 | P-04 |
| [UC-06](#uc-06) | Compare strategies on the leaderboard | A-01 | P-06 |
| [UC-07](#uc-07) | Inspect a strategy's trades | A-01 | P-07 |
| [UC-08](#uc-08) | Reproduce a past result | A-01 | P-09 |
| [UC-09](#uc-09) | Review news and sentiment | A-01 | P-10 |
| [UC-10](#uc-10) | Add a new strategy | A-02 | P-11 |
| [UC-11](#uc-11) | Add a new search method | A-02 | P-12 |
| [UC-12](#uc-12) | Add a new data source | A-02 | P-13 |
| [UC-13](#uc-13) | Monitor a running search | A-03 | P-14 |
| [UC-14](#uc-14) | Pause, resume or stop a search | A-03 | P-15 |
| [UC-15](#uc-15) | Recover from a lost data connection | A-03 | P-17 |
| [UC-16](#uc-16) | Load historical market data | A-01 | P-01 |

---

## Strategy Researcher (A-01)

### UC-01

**View live market charts**

- **Level:** User goal.
- **Primary actor:** [A-01](01-actors.md#a-01)
- **Supporting actors:** [A-04](01-actors.md#a-04)
- **Solves:** [P-08](02-problems.md#p-08)
- **Trigger:** The researcher opens the chart screen.
- **Preconditions:**
    - At least one market data provider is available.
- **Success guarantee:**
    - The researcher sees up to 4 charts with live prices, each with its own timeframe.
- **Minimal guarantee:**
    - The researcher is told which charts are not live.
- **Main success scenario:**
    1. The researcher chooses a pair.
    2. The researcher chooses a timeframe for each chart, up to 4 charts.
    3. The system shows recent candles on each chart.
    4. The system updates each chart as new prices arrive.
    5. The researcher changes the timeframe of one chart.
    6. The system updates only that chart.
- **Extensions:**
    - 3a. No data exists for the chosen pair or timeframe:
        1. The system tells the researcher and keeps the other charts.
    - 4a. The live connection drops:
        1. The system shows that the chart is not live.
        2. Continue with [UC-15](#uc-15).

### UC-02

**Run a backtest**

- **Level:** User goal.
- **Primary actor:** [A-01](01-actors.md#a-01)
- **Supporting actors:** none.
- **Solves:** [P-01](02-problems.md#p-01), [P-05](02-problems.md#p-05), [P-06](02-problems.md#p-06)
- **Trigger:** The researcher wants to know how a strategy would have done in the past.
- **Preconditions:**
    - Historical data for the chosen range is available ([UC-16](#uc-16)).
- **Success guarantee:**
    - A result is saved with every trade and all metrics.
    - The result is linked to the exact strategy version, data and settings.
- **Minimal guarantee:**
    - No partial or wrong result is saved.
- **Main success scenario:**
    1. The researcher chooses a strategy and its parameters.
    2. The researcher chooses a pair, a timeframe and a date range.
    3. The researcher sets the starting balance, fee rate and slippage.
    4. The system replays the candles in time order and records every trade.
    5. The system calculates the metrics.
    6. The system shows the result and saves it.
- **Extensions:**
    - 2a. The data has gaps:
        1. The system shows where the gaps are.
        2. The researcher chooses another range, or loads the missing data ([UC-16](#uc-16)).
    - 4a. The strategy makes no trades:
        1. The system saves the result with zero trades and says so.
    - 4b. The strategy fails with an error:
        1. The system stops the backtest and shows the error.

### UC-03

**Build a composite strategy**

- **Level:** User goal.
- **Primary actor:** [A-01](01-actors.md#a-01)
- **Supporting actors:** none.
- **Solves:** [P-02](02-problems.md#p-02), [P-10](02-problems.md#p-10)
- **Trigger:** The researcher wants to mix several strategies into one.
- **Preconditions:**
    - At least two strategies are available.
- **Success guarantee:**
    - A new composite strategy is saved and can be used anywhere a single strategy can.
- **Minimal guarantee:**
    - Existing strategies are not changed.
- **Main success scenario:**
    1. The researcher chooses two or more strategies.
    2. The researcher sets the parameters of each one.
    3. The researcher chooses a combination rule (e.g. majority vote, weighted score).
    4. The system checks that the composite is valid.
    5. The system saves the composite as a new strategy version.
- **Extensions:**
    - 1a. The researcher includes news sentiment as one of the inputs:
        1. The system treats sentiment like any other strategy signal.
    - 4a. The rule settings are invalid (e.g. weights do not add up):
        1. The system explains the problem.
        2. Return to step 3.

### UC-04

**Run a strategy search**

- **Level:** User goal.
- **Primary actor:** [A-01](01-actors.md#a-01)
- **Supporting actors:** none.
- **Solves:** [P-03](02-problems.md#p-03), [P-15](02-problems.md#p-15)
- **Trigger:** The researcher wants the system to find good combinations automatically.
- **Preconditions:**
    - Historical data for the chosen range is available.
- **Success guarantee:**
    - Every tested candidate has a saved result.
    - The leaderboard shows the best candidates found.
    - The run ends by its stop condition or by the operator.
- **Minimal guarantee:**
    - Results already saved are kept, even if the run fails.
- **Main success scenario:**
    1. The researcher defines the search space: strategies, parameter ranges and combination rules.
    2. The researcher chooses a search method.
    3. The researcher sets a stop condition.
    4. The system creates a candidate.
    5. The system tests the candidate with a walk-forward test ([UC-05](#uc-05)).
    6. The system updates the leaderboard.
    7. The system repeats steps 4–6 until the stop condition is met.
    8. The system reports that the run has ended and why.
- **Extensions:**
    - 3a. No stop condition is set:
        1. The system does not start the run and asks for one.
    - 4a. The search space is used up:
        1. The system ends the run and says so.
    - 5a. One candidate fails:
        1. The system records the error and continues with the next candidate.

### UC-05

**Run a walk-forward test**

- **Level:** Subfunction (used by [UC-04](#uc-04)). Can also be run alone.
- **Primary actor:** [A-01](01-actors.md#a-01)
- **Supporting actors:** none.
- **Solves:** [P-04](02-problems.md#p-04)
- **Trigger:** A strategy result must be checked on unseen data.
- **Preconditions:**
    - The date range is long enough for at least two test windows.
- **Success guarantee:**
    - The result is built only from test windows the strategy did not see when its parameters were chosen.
- **Minimal guarantee:**
    - No result is shown as walk-forward if any window failed.
- **Main success scenario:**
    1. The researcher chooses a strategy, its parameter ranges and a date range.
    2. The researcher sets the length of the tuning window and the test window.
    3. The system finds the best parameters on the first tuning window.
    4. The system tests those parameters on the next test window.
    5. The system moves both windows forward and repeats steps 3–4 to the end of the range.
    6. The system joins all test windows into one result and saves it.
- **Extensions:**
    - 1a. The range is too short:
        1. The system says how much more data is needed.

### UC-06

**Compare strategies on the leaderboard**

- **Level:** User goal.
- **Primary actor:** [A-01](01-actors.md#a-01)
- **Supporting actors:** none.
- **Solves:** [P-06](02-problems.md#p-06)
- **Trigger:** The researcher wants to know which strategies are best.
- **Preconditions:**
    - At least one result exists.
- **Success guarantee:**
    - The researcher sees the top strategies with profit, risk and cost metrics side by side.
- **Minimal guarantee:**
    - The leaderboard is never shown with stale data without a warning.
- **Main success scenario:**
    1. The researcher opens the leaderboard.
    2. The system shows the top K strategies with their metrics and overall score.
    3. The researcher sorts by a chosen metric.
    4. The system re-orders the list.
    5. The system updates the list while a search is running.
- **Extensions:**
    - 2a. The researcher asks how the score is calculated:
        1. The system shows the formula and the weight of each metric.

### UC-07

**Inspect a strategy's trades**

- **Level:** User goal.
- **Primary actor:** [A-01](01-actors.md#a-01)
- **Supporting actors:** none.
- **Solves:** [P-07](02-problems.md#p-07)
- **Trigger:** The researcher wants to see *what* a strategy did.
- **Preconditions:**
    - A saved result exists.
- **Success guarantee:**
    - The researcher sees every trade on the price chart, with the indicators the strategy used.
- **Minimal guarantee:**
    - The saved result is not changed.
- **Main success scenario:**
    1. The researcher chooses a result (e.g. from the leaderboard).
    2. The system shows the price chart for that result's pair, timeframe and range.
    3. The system draws the indicators the strategy used.
    4. The system marks every entry and exit on the chart.
    5. The system shows a list of all trades.
    6. The researcher chooses one trade.
    7. The system highlights that trade's entry and exit on the chart.

### UC-08

**Reproduce a past result**

- **Level:** User goal.
- **Primary actor:** [A-01](01-actors.md#a-01)
- **Supporting actors:** none.
- **Solves:** [P-09](02-problems.md#p-09)
- **Trigger:** The researcher doubts a past result, or wants to compare it with a new one.
- **Preconditions:**
    - The past result and its data are still stored.
- **Success guarantee:**
    - The new run gives exactly the same trades and metrics as the past result.
- **Minimal guarantee:**
    - The past result is not changed or overwritten.
- **Main success scenario:**
    1. The researcher chooses a past result.
    2. The system shows the exact strategy version, parameters, data range and settings used.
    3. The researcher asks to run it again.
    4. The system runs it with the same inputs.
    5. The system shows that the new result matches the old one.
- **Extensions:**
    - 5a. The results do not match:
        1. The system shows the differences and flags the past result as not reproducible.

### UC-09

**Review news and sentiment**

- **Level:** User goal.
- **Primary actor:** [A-01](01-actors.md#a-01)
- **Supporting actors:** [A-05](01-actors.md#a-05)
- **Solves:** [P-10](02-problems.md#p-10)
- **Trigger:** The researcher wants to know the news mood around a coin.
- **Preconditions:**
    - The system has collected news from at least one source.
- **Success guarantee:**
    - The researcher sees recent news for the coin, each with a sentiment label and score.
- **Minimal guarantee:**
    - If news is not available, the rest of the app still works.
- **Main success scenario:**
    1. The researcher chooses a coin.
    2. The system shows recent news about that coin.
    3. The system shows the sentiment of each news item.
    4. The system shows the share of positive, neutral and negative news.
- **Extensions:**
    - 2a. No news source is reachable:
        1. The system shows the last collected news and says when it was collected.

## Strategy Developer (A-02)

### UC-10

**Add a new strategy**

- **Level:** User goal.
- **Primary actor:** [A-02](01-actors.md#a-02)
- **Supporting actors:** none.
- **Solves:** [P-11](02-problems.md#p-11)
- **Trigger:** The developer wants a strategy that the system does not have (e.g. MACD).
- **Preconditions:**
    - The developer knows the rules of the new strategy.
- **Success guarantee:**
    - The new strategy can be used in backtests, composites, searches and charts.
    - No existing feature is broken.
- **Minimal guarantee:**
    - If the new strategy is broken, the other strategies still work.
- **Main success scenario:**
    1. The developer writes the new strategy, following the system's strategy contract.
    2. The developer declares its parameters and allowed ranges.
    3. The developer registers the strategy.
    4. The system lists the new strategy with the existing ones.
    5. The developer runs a backtest with it ([UC-02](#uc-02)) to check it.
- **Extensions:**
    - 3a. The name is already used:
        1. The system rejects the registration and says why.

### UC-11

**Add a new search method**

- **Level:** User goal.
- **Primary actor:** [A-02](01-actors.md#a-02)
- **Supporting actors:** none.
- **Solves:** [P-12](02-problems.md#p-12)
- **Trigger:** The developer wants a better way to search (e.g. a genetic algorithm).
- **Preconditions:**
    - At least one search method already works.
- **Success guarantee:**
    - The researcher can choose the new method when starting a search.
    - Testing, scoring and ranking work without change.
- **Minimal guarantee:**
    - The old search methods still work.
- **Main success scenario:**
    1. The developer writes the new search method, following the system's search contract.
    2. The developer registers it.
    3. The system lists it as a choice in [UC-04](#uc-04).
    4. The developer runs a short search with it to check it.

### UC-12

**Add a new data source**

- **Level:** User goal.
- **Primary actor:** [A-02](01-actors.md#a-02)
- **Supporting actors:** [A-04](01-actors.md#a-04) or [A-05](01-actors.md#a-05)
- **Solves:** [P-13](02-problems.md#p-13)
- **Trigger:** The developer wants prices from another provider, or news from another source.
- **Preconditions:**
    - The new source is reachable and its data format is known.
- **Success guarantee:**
    - Data from the new source appears in the same internal format as other sources.
    - Screens and strategies work without change.
- **Minimal guarantee:**
    - Existing sources still work.
- **Main success scenario:**
    1. The developer writes a translator from the source's format to the system's format.
    2. The developer registers the new source.
    3. The system collects data from it.
    4. The developer checks that the data appears in charts or news.
- **Extensions:**
    - 3a. The source sends data the translator cannot read:
        1. The system skips that item and records the error.

## Lab Operator (A-03)

### UC-13

**Monitor a running search**

- **Level:** User goal.
- **Primary actor:** [A-03](01-actors.md#a-03)
- **Supporting actors:** none.
- **Solves:** [P-14](02-problems.md#p-14)
- **Trigger:** A search is running and the operator wants to know its state.
- **Preconditions:**
    - A search has been started.
- **Success guarantee:**
    - The operator sees the current state of the run.
- **Minimal guarantee:**
    - Looking at the state does not slow down or change the run.
- **Main success scenario:**
    1. The operator opens the run status view.
    2. The system shows: state (running, paused, ended), candidates tested, candidates failed, time used and current best.
    3. The system updates these values while the run continues.
- **Extensions:**
    - 2a. Many candidates are failing:
        1. The system shows the most common errors.

### UC-14

**Pause, resume or stop a search**

- **Level:** User goal.
- **Primary actor:** [A-03](01-actors.md#a-03)
- **Supporting actors:** none.
- **Solves:** [P-15](02-problems.md#p-15)
- **Trigger:** The operator wants to control a run by hand.
- **Preconditions:**
    - A search is running or paused.
- **Success guarantee:**
    - The run is in the state the operator asked for.
    - All results finished before the request are kept.
- **Minimal guarantee:**
    - No saved result is lost or damaged.
- **Main success scenario:**
    1. The operator asks to pause the run.
    2. The system finishes the candidates already in progress, then pauses.
    3. The operator asks to resume.
    4. The system continues from where it stopped.
    5. The operator asks to stop.
    6. The system ends the run and reports why it ended.

### UC-15

**Recover from a lost data connection**

- **Level:** Subfunction (used by [UC-01](#uc-01)).
- **Primary actor:** [A-03](01-actors.md#a-03)
- **Supporting actors:** [A-04](01-actors.md#a-04)
- **Solves:** [P-17](02-problems.md#p-17)
- **Trigger:** The live connection to a market data provider drops.
- **Preconditions:**
    - The system was receiving live data.
- **Success guarantee:**
    - Live data flows again.
    - No candle is missing for the time the connection was down.
- **Minimal guarantee:**
    - The gap is recorded and shown, so no one uses data with a hidden gap.
- **Main success scenario:**
    1. The system notices that the connection has dropped.
    2. The system shows on the charts that data is not live.
    3. The system tries to reconnect.
    4. The connection comes back.
    5. The system fetches the candles missed during the gap.
    6. The system shows that data is live again.
- **Extensions:**
    - 3a. Reconnecting keeps failing:
        1. The system waits longer between tries.
        2. The system tells the operator that the provider is down.

### UC-16

**Load historical market data**

- **Level:** Subfunction (used by [UC-02](#uc-02), [UC-04](#uc-04), [UC-05](#uc-05)).
- **Primary actor:** [A-01](01-actors.md#a-01)
- **Supporting actors:** [A-04](01-actors.md#a-04)
- **Solves:** [P-01](02-problems.md#p-01)
- **Trigger:** A test needs candles that the system does not have yet.
- **Preconditions:**
    - A market data provider is reachable.
- **Success guarantee:**
    - All candles for the pair, timeframe and range are stored, with no gaps.
- **Minimal guarantee:**
    - Any gap is recorded and reported.
- **Main success scenario:**
    1. The researcher chooses a pair, a timeframe and a date range.
    2. The system checks which candles it already has.
    3. The system downloads only the missing candles.
    4. The system checks that there are no gaps.
    5. The system stores the candles.
- **Extensions:**
    - 3a. The provider limits the number of requests:
        1. The system slows down and continues.
    - 4a. Gaps remain (e.g. the provider has no data for that time):
        1. The system records the gaps and reports them.
