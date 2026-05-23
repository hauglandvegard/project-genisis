# Roadmap

## Bugs

- [x] Catch `GenesisError` in pre-prompt block (`get_user_info`, `get_template_owner_info`, `list_templates` can all raise it but only `KeyboardInterrupt` is caught)
- [x] Force fresh cookiecutter pull — currently may use cached template

## Polish

- [x] Extract `_fetch_github_user(endpoint)` helper to deduplicate `get_user_info` / `get_template_owner_info`
- [x] Remove `python-dotenv` or add actual env var usage (currently loaded but unused)
- [x] Show GitHub repo URL on success
- [x] Check dest dir doesn't already exist before scaffolding

## Features

- [x] `genesis list` — show available templates without scaffolding
- [x] `--no-push` flag — local scaffold only, skip GitHub repo creation
- [x] Open project in `$EDITOR` after scaffold

## Templates (`genesis-templates`)

- [x] Python / FastAPI
- [ ] Go — base
- [ ] Python / Flask
- [ ] Python / Django
- [ ] Go / Wails (+ Svelte or htmx)
- [ ] TypeScript
- [ ] React
- [ ] Shad/cn
- [ ] Next.js
- [ ] Express.js

## Infrastructure

- [x] Fix Dockerfile — add `gh`, `git`, `npx` dependencies
- [x] Update `docs/question-flow.md` to match current flow
