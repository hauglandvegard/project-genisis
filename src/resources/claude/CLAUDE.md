# CLAUDE.md

Project context for Claude Code. Drop this file and `.claude/` into a new project root together.

## Project

<!-- Replace with one-paragraph project description: what it does, who it's for, language/stack. -->

TBD — fill in when starting the project.

## Workflow

This project uses a 4-phase agent workflow driven by slash commands. Each phase has a single entry point; do not skip phases or run them out of order.

```
/brainstorm  →  docs/design.md  →  docs/plan.md
     ↓
/implement   →  branch + commits per task
     ↓
/merge       →  disposition (merge/PR/keep/discard)
```

### `/brainstorm [rough idea]`
Two-step: `brainstorm` agent drives a section-by-section design dialogue → `docs/design.md`. Then `planner` agent decomposes the design into goals and commit-sized tasks → `docs/plan.md` with checkboxes.

### `/implement`
Two-step: `git-master` sets up branch + verifies clean test baseline, then `lead-developer` drives `docs/plan.md` task-by-task. Each task gets a fresh `tdd-dev` (RED-GREEN-REFACTOR) and two-stage review by `code-reviewer`. Pauses after every task for `continue?`.

### `/merge`
Verifies tests, presents disposition options, cleans up the worktree.

## Agents

Located in `.claude/agents/`. Auto-discovered by Claude Code.

| Agent | Role | Model |
|---|---|---|
| `brainstorm` | Design dialogue → `docs/design.md` | opus |
| `planner` | `design.md` → `docs/plan.md` (goals + tasks) | opus |
| `git-master` | Branch setup, project install, clean baseline | sonnet |
| `lead-developer` | Orchestrates tasks, dispatches TDD devs, runs reviews | sonnet |
| `tdd-dev` | One task, strict RED-GREEN-REFACTOR, one commit | sonnet |
| `code-reviewer` | Two-stage review: spec compliance, then code quality | opus |
| `pr-manager` | Test + disposition + worktree cleanup | sonnet |

## Artifacts

| Path | Written by | Read by |
|---|---|---|
| `docs/design.md` | `brainstorm` | `planner` |
| `docs/plan.md` | `planner` | `lead-developer`, `tdd-dev` (task brief), `code-reviewer` |
| `logs/agents.log` | every agent | humans |

Log format: `<ISO-8601 time> <agent> <DEBUG|INFO|WARNING|ERROR|CRITICAL> <message>`

## Conventions

- **No internet access for subagents.** All language/framework knowledge comes from central `expert-*` agents in `~/.claude/agents/` (Docker, Go, Go-Wails, JS, HTMX, Python, FastAPI, Rust, TS, React, Svelte). If a question requires a language not covered, agents halt.
- **One task = one commit.** TDD devs never bundle.
- **Tests must pass before merge.** PR-manager enforces.
- **Plan is source of truth.** Lead developer does not invent tasks; if the plan is wrong, re-run `@planner`.

## Project-specific conventions

<!-- Replace this section with project-specific notes:
     - Test command (e.g., `npm test`, `pytest`, `go test ./...`)
     - Build command
     - Linter / formatter
     - Branch naming convention if non-default
     - Anything else recurring agents should know
-->

TBD.

## Setup checklist for a fresh project

1. Drop this `CLAUDE.md` and the `.claude/` folder into the project root.
2. Fill in the **Project** and **Project-specific conventions** sections above.
3. Run `/brainstorm <your idea>` to start.
