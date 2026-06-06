# vnstock-agent

Agent for Vietnamese stock market data interaction using Python, PydanticAI, Strategy/Factory pattern, and Logxide.

## Prerequisites

No system-level package manager (e.g., Homebrew) required — `uv` manages Python and dependencies.

## Setup Instructions

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. **Install Python 3.15** using uv:
   ```bash
   uv python install 3.15
   ```
3. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url> && cd vnstock-agent
   ```
4. **Create virtual environment** with Python 3.15:
   ```bash
   uv venv --python 3.15
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

This starts an interactive session:

```
vnstock-agent (type 'exit' to quit)
----------------------------------------

You: What is the P/E ratio of VNM?
Agent: [response]

You: exit
Goodbye!
```

### Add a new provider

To add a new LLM provider (e.g., OpenAI):

1. Create a strategy file `src/llm/strategies/<provider>.py` extending `BaseLLMStrategy`
2. Register it in `LLMFactory._strategies` dict in `src/llm/factory.py`
3. Add provider-specific settings to `src/config/settings.py`
4. Set `PROVIDER=<provider>` in `.env`

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

```
vnstock-agent/
├── .env                  # Local environment variables (do not commit)
├── .env.example          # Template for environment variables
├── .gitignore            # Git ignore rules
├── .venv/                # Python 3.15 virtual environment (created by uv)
├── pyproject.toml        # Project metadata and dependencies
├── README.md             # Project documentation and setup guide
├── structure.md          # This file: project structure overview
├── lefthook.yml          # Git hooks configuration
├── tests/                # Pytest test suite
│   ├── conftest.py       # Shared fixtures
│   └── unit/             # Unit tests
└── src/
    ├── agent/            # Agent core implementation
    │   ├── __init__.py
    │   ├── __main__.py   # Interactive CLI entry point
    │   ├── core/
    │   │   └── agent.py  # PydanticAI Agent with LLMFactory
    │   └── tools/        # Agent tools (future)
    ├── config/           # Application configuration
    │   ├── __init__.py
    │   └── settings.py   # Pydantic Settings loading .env
    ├── llm/              # LLM provider integrations
    │   ├── __init__.py   # Exposes LLMFactory
    │   ├── factory.py    # Factory pattern: creates strategy by PROVIDER env
    │   └── strategies/   # Strategy pattern: each provider is a strategy
    │       ├── __init__.py
    │       ├── base.py   # BaseLLMStrategy abstract class
    │       └── ollama.py # OllamaStrategy: OllamaModel + OllamaProvider
    └── utils/            # Reusable utilities
        ├── __init__.py
        └── logger/
            ├── __init__.py     # Exposes get_logger, ILogger
            ├── interface.py    # ILogger abstract interface
            ├── logger.py       # Factory: returns logger by LOGGER_TYPE
            └── logxide_adapter.py # Logxide adapter (JSON format with ms)
```

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
- Target Python version: 3.15
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
