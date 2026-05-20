## Goal
Build a CLI tool that initializes new projects in the terminal with the keyword `genesis`.

## Repos
- `project-genisis` — CLI tool (this repo, installable, runs `genesis` command)
- `genesis-templates` — separate repo, monorepo of all template directories

## Flow
```
genesis
  → fetch available templates from vegard/genesis-templates (subdir list)
  → select language   [Python | Go | TypeScript | ...]
  → select variant    [base | Flask | Django | ...]  ← filtered by language
  → enter project name
  → enter dest dir    (default: ~/Code/<name>)
  → select visibility (public / private)
  → scaffold          (cookiecutter or degit based on template type)
  → gh repo create + bind remote + push
```

## Scaffolding dispatch
- Template subdir starts with `python/` → **cookiecutter** (variable substitution via `cookiecutter.json`)
- All others → **degit** (`degit vegard/genesis-templates/<subdir> <dest>`)

## Tech
- `questionary` — interactive CLI prompts (select, text, confirm)
- `cookiecutter` — scaffold Python templates with variable substitution
- `npx degit` — scaffold Go / JS / TS templates
- `gh` CLI — list templates, create repo, push

## Template structure (`genesis-templates` repo)
```
genesis-templates/
  python/
    cookiecutter.json
    {{cookiecutter.project_name}}/
  go/
    cookiecutter.json
    {{cookiecutter.project_name}}/
  python-flask/
    cookiecutter.json
    {{cookiecutter.project_name}}/
  react/
  next/
  express/
  ...
```

## Code structure (`project-genisis`)
```
src/
  main.py      ← entry point, orchestrate flow
  cli.py       ← questionary prompts
  github.py    ← gh CLI wrapper (list subdirs, create repo, push)
  scaffold.py  ← cookiecutter / degit dispatch
  config.py    ← constants (template repo, default dest dir)
```

## Languages and frameworks

### Now
- Python
- Python / Fastapi
- Go

### Later
- Python / Flask
- Python / Django
- Go / Wails (+ Svelte or htmx)
- TypeScript
- React
- Shad/cn

### In the future
- Next.js
- Express.js
- Java
- Rust
- Vue
