# vnstock-agent
Agent for vnstock data interaction using Python, Pydantic Settings, and Logxide.

## Prerequisites
No system-level package manager (e.g., Homebrew) required - `uv` manages Python and dependencies.

## Setup Instructions
1. **Install uv** (if not already installed) via official standalone installer:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. **Install Python 3.12** using uv:
   ```bash
   uv python install 3.12
   ```
3. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url> && cd vnstock-agent
   ```
4. **Create virtual environment** with Python 3.12:
   ```bash
   uv venv --python 3.12
   ```
5. **Install project dependencies**:
   ```bash
   uv pip install -e .
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
Available environment variables (see `.env.example` for defaults):
- `APP_NAME`: Application name (default: `vnstock-agent`)
- `DEBUG`: Debug mode flag (default: `false`)
- `OLLAMA_BASE_URL`: Ollama base URL (default: `http://localhost:11434`)

## Project Structure
See [structure.md](structure.md) for full project layout.

## Usage
Run the Ollama provider to test settings and logger:
```bash
python -m llm.providers.ollama
```

## Code Quality: Ruff
This project uses [Ruff](https://github.com/astral-sh/ruff) for fast Python linting and formatting.

### Install Ruff
```bash
# Install in virtual environment
uv pip install ruff

# Or install as dev dependency (if using dependency groups)
uv pip install -e ".[dev]"
```

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
- Target Python version: 3.12
- Line length: 120
- Enabled rules: pycodestyle, pyflakes, warnings, isort, pyupgrade
