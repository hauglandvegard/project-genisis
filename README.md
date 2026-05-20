# template-python

Python project template.

## Prerequisites

[Install uv](https://docs.astral.sh/uv/getting-started/installation/)

## After cloning

1. Rename `name` in `pyproject.toml`
2. Update this README

## Setup

```bash
uv sync --group dev
cp .env.example .env
```

## Run

```bash
uv run python -m src.main
```

## Dev

```bash
uv run ruff format .
uv run ruff check .
uv run mypy src
uv run pytest
```
