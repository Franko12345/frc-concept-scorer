# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root — defines concepts (Concept, Criterion, Weight, Score), the scoring formula, the two run modes (Pages static + Flask dev), and known pitfalls.
- **`docs/adr/`** — read ADRs that touch the area you're about to work in.

If either doesn't exist, **proceed silently**.

## File structure

Single-context repo (this one):

```
/
├── AGENTS.md
├── CONTEXT.md
├── docs/
│   ├── agents/
│   │   ├── issue-tracker.md
│   │   ├── triage-labels.md
│   │   └── domain.md
│   └── adr/             ← ADRs land here
├── index.html
├── templates/
├── static/
├── scorer.py
├── app.py
└── test_scorer.py
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms.

If the concept you need isn't in the glossary yet, that's a signal — note it for `/domain-modeling`.

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding.
