# Issue tracker: GitHub

Issues and PRs for this repo live as GitHub issues and pull requests. Use the `gh` CLI for all operations.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body-file /tmp/issue-body-<slug>.md`. Use a file (not heredoc) — heredoc bodies trip the security scanner.
- **Read an issue**: `gh issue view <number> --comments`.
- **List issues**: `gh issue list --state open --json number,title,body,labels --jq '[.[] | {number, title, labels: [.labels[].name]}]'`.
- **Apply / remove labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`.
- **Close**: `gh issue close <number> --comment "..."`.

Infer the repo from `git remote -v` — `gh` does this automatically when run inside a clone.

## Pull requests as a triage surface

**PRs as a request surface: no.** External PRs do not enter the triage queue. The team is small and external contributions are not expected for an internal team tool.

## When a skill says "publish to the issue tracker"

Create a GitHub issue. Spec/ticket templates come from the `to-spec` and `to-tickets` skills.

## When a skill says "fetch the relevant ticket"

`gh issue view <number> --comments`.
