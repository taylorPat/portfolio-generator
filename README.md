# Portfolio Generator

A simple tool to generate a static portfolio site from structured data.

## 🚀 Setup

### Prerequisites

- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)

## ⚙️ Installation

```bash
git clone https://github.com/taylorPat/portfolio-generator
cd portfolio-generator
uv sync
uv pip install -e .
```

> Note: The editable install (`-e`) is currently required to enable the CLI.

## ▶️ Usage

```bash
uv run portfolio --docs-folder-path <DOCS_FOLDER_PATH>
```

- `<DOCS_FOLDER_PATH>`: Path where the generated site will be written
