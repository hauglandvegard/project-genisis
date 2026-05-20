# Roadmap

## Bugs

- [x] Catch `GenesisError` in pre-prompt block (`get_user_info`, `get_template_owner_info`, `list_templates` can all raise it but only `KeyboardInterrupt` is caught)
- [x] Force fresh cookiecutter pull — currently may use cached template

## Polish

- [ ] Extract `_fetch_github_user(endpoint)` helper to deduplicate `get_user_info` / `get_template_owner_info`
- [ ] Remove `python-dotenv` or add actual env var usage (currently loaded but unused)
- [ ] Show GitHub repo URL on success
- [ ] Check dest dir doesn't already exist before scaffolding

## Features

- [ ] `genesis list` — show available templates without scaffolding
- [ ] `--no-push` flag — local scaffold only, skip GitHub repo creation
- [ ] Open project in `$EDITOR` after scaffold

## Templates (`genesis-templates`)

- [ ] Python / FastAPI
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

- [ ] Fix Dockerfile — add `gh`, `git`, `npx` dependencies
- [ ] Update `docs/question-flow.md` to match current flow
