# Project Genesis

CLI tool for initializing new projects on macOS. Scaffolds from a template, creates a GitHub repo, and opens the project in your editor.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [just](https://github.com/casey/just)
- [gh](https://cli.github.com/) — authenticated (`gh auth login`)
- [Zed](https://zed.dev/) or another editor with `$EDITOR` set

## Install

```bash
uv tool install .
```

## Usage

```bash
genesis              # scaffold + create GitHub repo + open in editor
genesis --no-push    # scaffold locally only
genesis list         # list available templates
```

## Editor

Set `$EDITOR` in `~/.zshrc` to auto-open the project after scaffold:

```zsh
export EDITOR=zed
```

## Dev

```bash
uv sync --group dev
just check
```

## Docker

```bash
docker build -t genesis .
docker run -it --rm \
  -v ~/.config/gh:/root/.config/gh \
  -v ~/Code:/root/Code \
  genesis
```
