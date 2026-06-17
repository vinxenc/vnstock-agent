# Project Structure

```
vnstock-agent/
├── .env.example          # Template for environment variables
├── .gitignore            # Git ignore rules
├── lefthook.yml          # Git hook configuration
├── pyproject.toml        # Project metadata, dependencies, and Ruff settings
├── README.md             # Project documentation and setup guide
├── structure.md          # This file: project structure overview
├── uv.lock               # uv dependency lockfile
├── tests/                # Unit and integration tests
│   ├── conftest.py       # Shared pytest fixtures
│   └── unit/
│       ├── agent/
│       ├── config/
│       ├── llm/
│       ├── market_data/
│       └── utils/
└── src/
    ├── agent/            # Interactive agent application
    │   ├── __init__.py
    │   ├── __main__.py   # CLI entry point: python -m agent
    │   ├── core/
    │   │   └── agent.py  # PydanticAI Agent configuration
    │   └── tools/
    │       └── market_data.py # Stock price/history agent tools
    ├── config/           # Application configuration
    │   ├── __init__.py
    │   └── settings.py   # Pydantic Settings loading .env
    ├── llm/              # LLM provider strategy/factory layer
    │   ├── __init__.py
    │   ├── factory.py    # Selects the configured LLM strategy
    │   └── strategies/
    │       ├── __init__.py
    │       ├── base.py   # Base strategy interface
    │       └── ollama.py # Ollama model strategy
    ├── market_data/      # Market data provider strategy/factory layer
    │   ├── README.md     # Package overview, architecture, adding a provider
    │   ├── __init__.py
    │   ├── factory.py    # Selects the configured market data provider
    │   ├── models.py     # Provider-agnostic StockPrice / StockPriceHistory
    │   └── providers/
    │       ├── __init__.py
    │       ├── base.py    # Base provider interface
    │       └── vnstock.py # vnstock-backed provider
    └── utils/            # Reusable utilities
        ├── __init__.py
        └── logger/
            ├── README.md
            ├── __init__.py
            ├── interface.py       # Logger interface
            ├── logger.py          # Logger factory
            └── logxide_adapter.py # Logxide logger adapter
```

Generated directories such as `__pycache__/`, `.ruff_cache/`, `.venv/`, and `*.egg-info/` are intentionally omitted from the source structure.
