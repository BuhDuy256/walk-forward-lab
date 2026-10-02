# Actors

## Writing rules

Based on: Alistair Cockburn, *Writing Effective Use Cases* (actor types).

**Meaning**

1. An actor is a **role**, not a person. One person can play many roles. Example: I am both A-01 and A-02.
2. An actor is **outside** the system. The system itself is never an actor.
3. Every actor has one type:
    - **Primary**: starts a use case to reach a goal.
    - **Supporting**: gives a service to the system (data, news). Often an external system.
    - **Offstage**: cares about the result but never touches the system.
4. A human actor must have at least one goal. A supporting actor has no goals. It has what it **gives** and what it **brings** (limits, failures).
5. External systems are named by their **role**, not by a product. Product names appear only as examples, in brackets.
6. An actor exists only if at least one problem (P-xx) or use case (UC-xx) needs it.

**Format**

7. IDs: `A-01`, `A-02`… An ID never changes and is never reused. A removed actor is marked **Withdrawn**, not deleted.
8. Each actor is one `###` heading with its ID, a bold name, then a bullet list of fields.
9. Use bullet lists. Do not put several ideas on one line.

**Links**

10. This file is the top of the chain: Actors → Problems → Use Cases → Spec.
11. Other files point **up** to this file. This file does not list links down.

---

## Index

| ID | Name | Type |
|---|---|---|
| [A-01](#a-01) | Strategy Researcher | Primary, human |
| [A-02](#a-02) | Strategy Developer | Primary, human |
| [A-03](#a-03) | Lab Operator | Primary, human |
| [A-04](#a-04) | Market Data Provider | Supporting, external system |
| [A-05](#a-05) | News Source | Supporting, external system |

---

### A-01

**Strategy Researcher**

- **Type:** Primary, human.
- **Description:** A person who studies trading strategies and uses the app every day.
- **Goals:**
    - Test strategy ideas fast.
    - Compare strategies fairly.
    - Trust the results.
    - Understand *why* a strategy did well or badly.

### A-02

**Strategy Developer**

- **Type:** Primary, human.
- **Description:** A person who extends the system with new parts. Example: a lecturer who asks to add a new strategy.
- **Goals:**
    - Add a new strategy with very little change to existing code.
    - Add a new search method with very little change.
    - Add a new data source with very little change.

### A-03

**Lab Operator**

- **Type:** Primary, human.
- **Description:** The person who starts, watches and stops long search runs.
- **Goals:**
    - See what a running search is doing.
    - Stop a bad or useless run early.
    - Keep the system running when a part fails.

### A-04

**Market Data Provider**

- **Type:** Supporting, external system. There can be more than one (e.g. a crypto exchange such as Binance).
- **Gives:**
    - Historical candles.
    - Live price updates.
- **Brings:**
    - Connection drops.
    - Rate limits.
    - Its own data format.

### A-05

**News Source**

- **Type:** Supporting, external system. There can be more than one (e.g. an RSS feed, a news API, a website).
- **Gives:**
    - News articles about coins.
- **Brings:**
    - A different format for each source.
    - Sources that change or disappear.
