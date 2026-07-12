# vnstock-agent

Conversational agent for Vietnamese stock market data, built with Python, PydanticAI, and a Strategy/Factory provider architecture. It fetches live prices via [vnstock](https://github.com/thinh-vu/vnstock) and runs as an interactive CLI.

## Prerequisites

No system-level package manager (e.g., Homebrew) required — `uv` manages Python and dependencies.

## Setup Instructions

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. **Install Python 3.14** using uv:
   ```bash
   uv python install 3.14
   ```
3. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url> && cd vnstock-agent
   ```
4. **Create virtual environment** with Python 3.14:
   ```bash
   uv venv --python 3.14
   ```
5. **Install project dependencies**:
   ```bash
   uv sync
   ```

## Activate Environment

Activate the virtual environment for your shell:

- **Bash/Zsh**:
  ```bash
  source .venv/bin/activate
  ```
- **Fish**:
  ```bash
  source .venv/bin/activate.fish
  ```
- **PowerShell**:
  ```bash
  .venv/bin/Activate.ps1
  ```

## Configuration

Copy `.env.example` to `.env` and adjust settings:

```bash
cp .env.example .env
```

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | `vnstock-agent` | Application name |
| `DEBUG` | `false` | Debug mode flag |
| `PROVIDER` | `ollama` | LLM provider (Strategy pattern) |
| `OLLAMA_BASE_URL` | `http://localhost:11434/v1` | Ollama OpenAI-compatible endpoint |
| `OLLAMA_MODEL` | `gpt-oss:120b-cloud` | Ollama model name |
| `MARKET_DATA_PROVIDER` | `vnstock` | Market data provider (Strategy pattern) |
| `VNSTOCK_SOURCE` | `VCI` | vnstock data source (e.g. `VCI`, `TCBS`) |
| `VNSTOCK_HISTORY_WINDOW_DAYS` | `30` | Lookback window (days) for latest-price lookups |
| `LOG_LEVEL` | `INFO` | Logging level |
| `LOGGER_TYPE` | `logxide` | Logger implementation |

### Provider: Ollama

1. Ensure Ollama is running locally:
   ```bash
   ollama serve
   ```
2. Pull the desired model:
   ```bash
   ollama pull gpt-oss:120b-cloud
   ```
3. Set env in `.env`:
   ```env
   PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434/v1
   OLLAMA_MODEL=gpt-oss:120b-cloud
   ```
   > **Note:** `OLLAMA_BASE_URL` must include `/v1` (Ollama's OpenAI-compatible endpoint).

## Usage

### Run the agent

```bash
uv run python -m agent
```

Run this from the repository root so `uv` uses the project virtual environment and `.env` is loaded from the expected location.

This launches [PydanticAI's interactive CLI](https://pydantic.dev/docs/ai/integrations/cli/). Ask for a stock price and the agent calls the `get_stock_price` tool, which fetches live data via vnstock. Responses render as markdown, and slash commands are available: `/exit`, `/markdown`, `/multiline`, `/cp`.

```text
vnstock-agent ➤ What is the latest price of FPT?
The latest price of FPT (FPT Corporation) is VND 73.20 per share (as of 2026-06-16).

vnstock-agent ➤ /exit
Exiting…
```

> **Note:** The agent has live stock-data tools wired in — `get_stock_price` and `get_stock_history`, backed by [vnstock](https://github.com/thinh-vu/vnstock). Ask e.g. *"What's the latest price of FPT?"* to fetch real market data. See [src/market_data/README.md](src/market_data/README.md) for the provider architecture. Live calls require Ollama running with a **tool-capable** model (e.g. `gpt-oss:120b-cloud`); models without tool-calling support won't trigger the price tools.

### Run API examples

**Web UI** (`src/api/web.py`) — serves a web chat interface using `to_web()`:

```bash
uv run granian src.api.web:app --host 127.0.0.1 --port 7932 --interface asgi
```

- Open `http://127.0.0.1:7932/` in browser for the chat UI
- API endpoint: `POST /api/chat` (Vercel AI protocol)

**AG-UI streaming** (`src/api/main.py`) — FastAPI server with AG-UI protocol:

```bash
uv run granian src.api.main:app --host 127.0.0.1 --port 7933 --interface asgi
```

- API endpoint: `POST /` (AG-UI protocol with SSE streaming)

Both examples reuse the core agent from `src/agent/core/agent.py`.

### Run with Docker

The AG-UI server (`src/api/main.py`) is packaged for containerized deployment. Use
Compose to build and run it with an explicit memory bound and a healthcheck:

```bash
docker compose up --build   # serves POST / on http://localhost:7933
```

- `mem_limit: 512m` caps the container — the app idles ~230 MiB and grows by the
  pandas/vnstock working set on the first tool call, so 512 MiB leaves headroom.
- `MALLOC_ARENA_MAX=2` (set in the `Dockerfile`) caps glibc arenas so the sync-tool
  thread pool doesn't inflate RSS.
- Requires a `.env` (see `.env.example`); Ollama must be reachable at `OLLAMA_BASE_URL`.

### Add a new provider

**LLM provider** (e.g., OpenAI):

1. Create a strategy file `src/llm/strategies/<provider>.py` extending `BaseLLMStrategy`
2. Add a `case` for it in `LLMFactory.create_strategy()` in `src/llm/factory.py`
3. Add provider-specific settings to `src/config/settings.py`
4. Set `PROVIDER=<provider>` in `.env`

**Market-data provider** (e.g., another stock API): see [src/market_data/README.md](src/market_data/README.md).

## Testing

Test dependencies are installed with the dev dependency group:

```bash
uv sync --dev
```

Run the full test suite:

```bash
uv run pytest
```

Run tests in parallel with `pytest-xdist`:

```bash
uv run pytest -n auto
```

Run unit tests only:

```bash
uv run pytest tests/unit
```

Run tests with coverage:

```bash
uv run pytest tests/unit --cov=src --cov-report=term-missing --cov-fail-under=90.01
```

Skip tests that require external services such as Ollama or network APIs:

```bash
uv run pytest -m "not external"
```

Disable `pytest-sugar` output formatting for plain pytest output:

```bash
uv run pytest -p no:sugar
```

Unit tests block real PydanticAI model requests by default and use test models/mocks instead of calling Ollama.

## Project Structure

See [structure.md](structure.md) for the full source tree. It is kept in sync with the repo and is the single source of truth for project layout.

## Code Quality: Ruff

This project uses [Ruff](https://github.com/astral-sh/ruff) for fast Python linting and formatting.

### Format Code

```bash
ruff format .
```

### Lint Code

```bash
# Check for issues
ruff check .

# Auto-fix issues
ruff check --fix .
```

### Configuration

Ruff settings are defined in `pyproject.toml` under `[tool.ruff]`:
- Target Python version: 3.14
- Line length: 120
- Enabled rules: pycodestyle, pyflakes, warnings, isort, pyupgrade

## Git Hooks: Lefthook

This project uses [Lefthook](https://github.com/evilmartians/lefthook) to automate code quality checks.

### Initialize Hooks

```bash
lefthook install
```

This sets up `pre-commit` and `pre-push` hooks.

### What Runs Automatically?

- **Pre-commit**:
  - `ruff format` (formats staged Python files)
  - `ruff check --fix` (auto-fixes lint issues in staged files)
  - `pytest tests/unit --cov=src --cov-report=term-missing --cov-fail-under=90.01`
- **Pre-push**:
  - `ruff check` (checks all Python files before push)
  - `pytest tests/unit --cov=src --cov-report=term-missing --cov-fail-under=90.01`

### Skip Hooks (Emergency Only)

```bash
git commit -m "message" --no-verify
git push --no-verify
```
