# FRC Concept Scorer — Agent Instructions

Multi-criteria decision app to help FRC teams pick the best robot concept for the next season.

## Agent skills

### Issue tracker

GitHub Issues (this repo). Use `gh issue` and `gh pr` for all ops. See `docs/agents/issue-tracker.md`.

### Triage labels

Five canonical roles (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context (root `CONTEXT.md` + `docs/adr/`). See `docs/agents/domain.md`.

## Workflow

We follow **Matt Pocock's Spec-Driven Development** loop:

1. **Plan** — `.hermes/plans/YYYY-MM-DD_HHMMSS-slug.md`, 2-5 min bite-sized tasks.
2. **Spec** — `to-spec` publishes parent issue labelled `ready-for-agent`.
3. **Tickets** — `to-tickets` breaks spec into vertical slices on the same tracker.
4. **Loop** — `feature-loop` ships each ticket: claim → branch → TDD → commit → PR → 3-reviewer fanout → squash-merge → close.

## Per-ticket review shape

Three parallel reviewers per PR (user convention since 2026-08):

- **Ponytail** — over-engineering only.
- **Matt Pocock standards** — style/spec adherence.
- **Third** — Correctness, Security, or Performance (pick per ticket).

Findings aggregated into a single report; only items that justify a code change are kept (no padding).

## Local dev

```bash
# static (same as Pages)
python3 -m http.server 8000
# open http://localhost:8000/

# Flask dev (uses data.json)
source .venv/bin/activate
python app.py
# open http://localhost:5050

# tests
pytest test_scorer.py -v
```
