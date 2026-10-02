# walk-forward-lab

A lab to build, combine and backtest crypto trading strategies, with walk-forward testing to check if a result is real.

## Working on → Read first

| Working on                    | Read first                                                                                  |
| ----------------------------- | ------------------------------------------------------------------------------------------- |
| Anything                      | [docs/00-vision/00-vision.md](docs/00-vision/00-vision.md) — what the system is for, and what is out of scope; [docs/01-glossary/01-glossary.md](docs/01-glossary/01-glossary.md) — the words |
| Requirements                  | [docs/02-requirements/AGENTS.md](docs/02-requirements/AGENTS.md)                             |
| Architecture decisions        | `docs/03-adr/`                                                                              |
| Design                        | `docs/04-architecture/`                                                                     |
| A day's log                   | `docs/05-journal/` — one file per day                                                       |
| Experiment reports            | `docs/06-experiments/`                                                                      |

## Rules for every area

1. Use the glossary words. If a word is not in the glossary, add it there first.
2. Never commit a secret: no API key, no exchange credential, no private data.
3. Do not commit. Leave the change in the working tree; the person reviews it.
