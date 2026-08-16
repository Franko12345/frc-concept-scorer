# FRC Concept Scorer — Domain Context

## What this is

Web app that helps an FRC robotics team rank competing robot concepts for an upcoming season using a weighted multi-criteria score.

## Core concepts

- **Concept** — a candidate robot architecture (e.g. "Turret shooter + floor intake", "Simple fixed shooter + hopper"). Has a name, optional description, and 4 raw scores.
- **Criterion** — a dimension along which concepts are evaluated. Four exist:
  - `pontos_potenciais` — how many match points the design could realistically score (HIGHER is better)
  - `complexidade` — engineering / build complexity (LOWER is better)
  - `risco` — probability of failure / unknown unknowns (LOWER is better)
  - `recursos` — material, budget, and people-hours required (LOWER is better)
- **Weight** — per-criterion importance (default 1.0). User can adjust.
- **Score** — final 0-10 weighted average, higher = better. Used to rank concepts.

## How scoring works

For each concept:
```
for each criterion k with raw value v and weight w:
    if k is "inverted" (complexidade, risco, recursos):
        v = 10 - v       # flip so LOW raw = HIGH score
    total += v * w
    wsum  += w
score = round(total / wsum, 2)
```

Three of the four criteria are inverted. `pontos_potenciais` is the only one where "more raw = better".

## Two run modes

1. **GitHub Pages (primary)** — `index.html` + `static/app.js` + `static/style.css`. 100% client-side, state in `localStorage` under key `frc-concept-scorer-v1`.
2. **Flask dev server (local)** — `app.py` mounts `templates/index.html`, exposes REST API at `/api/concepts`, persists to `data.json`.

The two share `scorer.py` (Python) — `static/app.js` is a faithful port of that logic. **They must stay in sync.** If you change the scoring algorithm, update both.

## Why the JS port exists

GitHub Pages only serves static content — it can't run Flask. The JS port lets the team access the tool from any browser without backend infra, while keeping the Flask version available for richer features later.

## Pitfalls / lessons

- **GitHub Pages + Flask = no-go.** The CI pipeline must deploy static files only; the workflow copies `index.html`, `static/`, and (if updated) `templates/` redirect stub.
- **JS and Python scoring must match.** Treat `scorer.py` as the source of truth — port changes to JS the same commit.
- **Branch protection requires CI green first.** We shipped the workflow and verified green on `main` before enabling `required_status_checks`.
- **localStorage is per-browser.** Concepts added on phone don't appear on laptop. Acceptable for current scope; team-wide sharing would need a backend.
