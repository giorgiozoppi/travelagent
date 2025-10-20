# Travel Agent - Parallelization Pattern Example

This project demonstrates the **Parallelization agentic pattern** using LangGraph. The pattern executes multiple independent operations simultaneously to improve efficiency and performance.

## Features

- **Parallel Agent Execution**: Concurrent execution of flight, hotel, events, restaurant, attractions, and social places searches
- **AI-Powered Analysis**: LLM-based analysis and consolidation of search results
- **Human-in-the-Loop**: Interactive approval workflow for travel plans
- **Type Safety**: Full type hints and py.typed support
- **Google Style Guide**: Code follows Google's Python style guide
- **Comprehensive Testing**: Unit and integration tests with coverage reporting

## Project Structure

```
travelagent/
├── travelagent/           # Main package
│   ├── __init__.py       # Package initialization
│   ├── models.py         # Data models and mock API functions
│   ├── parallel_agents.py # Parallel agent implementations
│   ├── main.py           # Main workflow and CLI
│   └── py.typed          # Type marker file
├── tests/                # Test suite
│   ├── unit/            # Unit tests
│   │   ├── test_models.py
│   │   ├── test_parallel_agents.py
│   │   └── test_main.py
│   ├── integration/     # Integration tests
│   │   ├── test_workflow.py
│   │   └── test_end_to_end.py
│   └── conftest.py      # Shared test fixtures
├── .github/
│   └── workflows/
│       └── ci.yml       # GitHub Actions CI/CD
├── pyproject.toml       # Project configuration
├── Makefile             # Development commands
└── README.md            # This file
```

## Installation

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

The Makefile **automatically detects** whether `uv` is installed and uses it; otherwise falls back to `pip`.

### Quick Start

```bash
# Install uv (optional but recommended for faster installs)
make install-uv

# Install dev dependencies (auto-detects uv or pip)
make install-dev
```

### Using uv (Recommended for Speed)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv

# Install dependencies
uv pip install -e ".[dev]"

# Or using make (auto-detects uv)
make install-dev
```

### Using pip

```bash
# Install dependencies
pip install -e ".[dev]"

# Or using make (auto-detects pip when uv not available)
make install-dev
```

### Check Current Package Manager

```bash
# See which package manager make will use
make help
# Output shows: "Current package manager: uv pip" or "Current package manager: pip"
```

## Configuration

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your-openai-api-key-here
```

## Usage

### Running the Application

```bash
# Using make
make run

# Or directly
python -m travelagent.main
```

### Development Commands

The project includes a Makefile with common development tasks:

```bash
# Show all available commands
make help

# Install dependencies
make install-dev

# Run all tests
make test

# Run unit tests only
make test-unit

# Run integration tests only
make test-integration

# Run tests with coverage report
make test-cov

# Lint code
make lint

# Format code
make format

# Type check
make type-check

# Run all checks (lint, format, type-check)
make check

# Clean build artifacts
make clean

# Build package
make build
```

## Testing

### Running Tests

```bash
# All tests
pytest -v

# Unit tests only
pytest tests/unit -v

# Integration tests only
pytest tests/integration -v

# With coverage report
pytest --cov=travelagent --cov-report=html --cov-report=term-missing
```

### Test Structure

- **Unit Tests** (`tests/unit/`): Test individual functions and components in isolation
- **Integration Tests** (`tests/integration/`): Test the complete workflow and agent interactions
- **Fixtures** (`tests/conftest.py`): Shared test data and mock objects

## Code Quality

### Linting and Formatting

The project uses **ruff** for both linting and formatting:

```bash
# Check code
ruff check .

# Format code
ruff format .
```

### Type Checking

The project uses **mypy** for static type checking:

```bash
mypy travelagent/
```

### Style Guide

Code follows **Google's Python Style Guide** with:
- Line length: 100 characters
- Google-style docstrings
- Type hints on all functions
- Sorted imports (isort)

## CI/CD

The project includes **three GitHub Actions workflows** that test both `uv` and `pip` installation methods:

### Workflows

1. **[ci.yml](.github/workflows/ci.yml)** - Main CI workflow using uv (default)
2. **[ci-uv.yml](.github/workflows/ci-uv.yml)** - Explicitly tests with uv package manager
3. **[ci-pip.yml](.github/workflows/ci-pip.yml)** - Explicitly tests with standard pip

Each workflow runs on every push and pull request:

- **Lint and Type Check**: Runs ruff and mypy on Python 3.10, 3.11, 3.12
- **Unit Tests**: Runs tests in `tests/unit/`
- **Integration Tests**: Runs tests in `tests/integration/`
- **Coverage**: Generates coverage reports and uploads to Codecov
- **Build**: Builds the package and uploads artifacts

This ensures the package works correctly with **both uv and pip** package managers.

## Architecture

### Parallelization Pattern

The travel agent uses LangGraph's parallelization capabilities to execute multiple search agents concurrently:

1. **Parallel Agents** (executed simultaneously):
   - Flight search agent
   - Hotel search agent
   - Events search agent
   - Restaurant search agent
   - Attractions search agent
   - Social places search agent

2. **Consolidation Agent**: Combines all search results into a comprehensive travel plan

3. **Human-in-the-Loop**: Presents the plan to the user for approval/modification

### Data Flow

```
User Input → Parallel Agents → Consolidation → Human Approval → Final Plan
              ├─ Flight
              ├─ Hotel
              ├─ Events
              ├─ Restaurant
              ├─ Attractions
              └─ Social Places
```

## Dependencies

### Core Dependencies
- `langgraph>=0.0.40` - Graph-based workflow orchestration
- `langchain-openai>=0.1.0` - OpenAI LLM integration
- `langchain-core>=0.1.0` - Core LangChain functionality
- `openai>=1.0.0` - OpenAI API client
- `rich>=13.0.0` - Beautiful terminal output
- `python-dotenv>=1.0.0` - Environment variable management

### Development Dependencies
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `pytest-mock>=3.10.0` - Mocking utilities
- `ruff>=0.1.0` - Linting and formatting
- `mypy>=1.0.0` - Static type checking

## Contributing

1. Install development dependencies: `make install-dev`
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Run code quality checks: `make check`
6. Commit your changes following the existing style
7. Submit a pull request

## License

This project is part of the agentic-patterns examples.

## Author

Giorgio Zoppi <giorgio.zoppi@gmail.com>
