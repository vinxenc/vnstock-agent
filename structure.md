# Project Structure

```
vnstock-agent/
├── .env                  # Local environment variables (do not commit)
├── .env.example          # Template for environment variables
├── .gitignore            # Git ignore rules
├── .venv/                # Python 3.12 virtual environment (created by uv)
├── pyproject.toml        # Project metadata and dependencies
├── README.md             # Project documentation and setup guide
├── structure.md           # This file: project structure overview
├── .git/                 # Git repository data
└── src/
    ├── agent/            # Agent core implementation
    │   ├── __init__.py
    │   ├── core/
    │   │   └── agent.py
    │   └── tools/
    ├── config/           # Application configuration
    │   ├── __init__.py
    │   └── settings.py   # Pydantic Settings loading .env
    ├── llm/              # LLM provider integrations
    │   ├── __init__.py
    │   └── providers/
    │       ├── __init__.py
    │       └── ollama.py # Ollama provider with settings/logger
    └── utils/            # Reusable utilities
        ├── __init__.py
        └── logger/
            ├── __init__.py
            └── logxide.py # Logxide logger wrapper
```
