# Project Genesis

CLI tool for initializing new projects on macOS. Run `genesis` in the terminal to scaffold a new project from a template.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [just](https://github.com/casey/just)
- [gh](https://cli.github.com/)

## Setup

```bash
uv sync --group dev
cp .env.example .env
```

## Run

```bash
genesis
```

## Dev

```bash
just check
```

## Install globally

```bash
uv tool install .
```
