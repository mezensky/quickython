# quickython

A quick start Python project template with modern development tools and best practices configured out of the box.

## Features

### Core Development Tools
- Modern project structure with `src/` layout
- Poetry for dependency management
- Fast linting and formatting with **Ruff** (replaces black, isort, flake8)
- Static type checking with **mypy**
- Comprehensive **pytest** suite with parallel execution and coverage

### Code Quality & Security
- **Security scanning** with pip-audit and Ruff security rules
- **Property-based testing** with Hypothesis
- **Docstring coverage** checking with interrogate
- **Dead code detection** with vulture
- **Coverage enforcement** (minimum 80%)

### Automation & CI/CD
- Pre-commit hooks for commit-time quality checks
- Pre-push hooks for test enforcement
- GitHub Actions CI/CD pipeline
- Dependabot for automated dependency updates
- Semantic versioning with Commitizen

### Developer Experience
- VS Code settings and dev container configuration
- Comprehensive Makefile for common tasks
- Build and publish tools for PyPI distribution
- Requirements.txt export for legacy compatibility

## Prerequisites

- Python 3.14 or higher
- Poetry (Python package manager)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd quickython
```

2. Install dependencies and set up pre-commit hooks:
```bash
make install
```

This will:
- Install all project dependencies using Poetry
- Set up pre-commit hooks to run automatically before each commit

## Development

### Running Tests

Run all tests (with parallel execution):
```bash
make test
```

Run tests with detailed coverage report:
```bash
make test-cov
```

Run tests without parallel execution:
```bash
make test-no-parallel
```

This generates both a terminal report and an HTML report in `htmlcov/`. Tests run in parallel by default using pytest-xdist for faster execution.

### Code Formatting

Format code automatically:
```bash
make format
```

This runs:
- `ruff check --fix` to auto-fix linting issues
- `ruff format` to format code

### Linting

Check code quality without making changes:
```bash
make lint
```

This runs:
- `ruff check` for fast linting (replaces flake8 + isort)
- `ruff format --check` to verify code formatting
- `mypy` for static type checking

### Pre-commit Hooks

Run all pre-commit hooks manually:
```bash
make pre-commit
```

Pre-commit hooks automatically run before each commit and include:
- Trailing whitespace removal
- End-of-file fixer
- YAML/TOML syntax checking
- Fast linting and formatting (ruff)
- Type checking (mypy)

### Security Scanning

Check for vulnerabilities in dependencies:
```bash
make security
```

### Code Quality Checks

Check docstring coverage:
```bash
make docs-check
```

Find unused/dead code:
```bash
make dead-code
```

### Version Management

Bump version (semantic versioning):
```bash
make bump-patch  # 0.1.0 -> 0.1.1
make bump-minor  # 0.1.0 -> 0.2.0
make bump-major  # 0.1.0 -> 1.0.0
```

Generate changelog:
```bash
make changelog
```

### Building & Publishing

Build distribution packages:
```bash
make build
```

Publish to Test PyPI:
```bash
make publish-test
```

Publish to PyPI:
```bash
make publish
```

Export requirements files:
```bash
make export-requirements
```

### Cleaning Build Artifacts

Remove build artifacts and caches:
```bash
make clean
```

## Project Structure

```
quickython/
├── src/
│   └── quickython/          # Main package
│       ├── __init__.py
│       └── sample.py
├── tests/                   # Test files
│   ├── __init__.py
│   └── test_sample.py
├── CLAUDE.md               # Setup history & context for Claude AI
├── pyproject.toml          # Project configuration
├── poetry.lock             # Locked dependencies
├── Makefile               # Development commands
├── .pre-commit-config.yaml # Pre-commit hooks config
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

> **Note for AI assistants**: See [CLAUDE.md](CLAUDE.md) for detailed setup history, completed configurations, and recommendations for next steps.

## Available Make Commands

### Essential Commands
| Command | Description |
|---------|-------------|
| `make install` | Install dependencies and set up pre-commit hooks |
| `make test` | Run all tests (parallel, with coverage enforcement) |
| `make lint` | Run all linters and type checkers |
| `make format` | Auto-format code with Ruff |

### Testing & Coverage
| Command | Description |
|---------|-------------|
| `make test` | Run tests in parallel with coverage |
| `make test-cov` | Run tests with detailed coverage report |
| `make test-no-parallel` | Run tests sequentially |

### Code Quality
| Command | Description |
|---------|-------------|
| `make security` | Scan dependencies for vulnerabilities |
| `make docs-check` | Check docstring coverage |
| `make dead-code` | Find unused code |
| `make pre-commit` | Run all pre-commit hooks manually |

### Version Management
| Command | Description |
|---------|-------------|
| `make bump-patch` | Bump patch version (0.1.0 → 0.1.1) |
| `make bump-minor` | Bump minor version (0.1.0 → 0.2.0) |
| `make bump-major` | Bump major version (0.1.0 → 1.0.0) |
| `make changelog` | Generate changelog |

### Build & Publish
| Command | Description |
|---------|-------------|
| `make build` | Build distribution packages |
| `make publish-test` | Publish to Test PyPI |
| `make publish` | Publish to PyPI |
| `make export-requirements` | Export requirements.txt files |

### Maintenance
| Command | Description |
|---------|-------------|
| `make clean` | Remove build artifacts and caches |

## Configuration

All tool configurations are centralized in `pyproject.toml`:

- **Ruff**: Line length 88, Python 3.13+ target, comprehensive rule sets (E, W, F, I, N, UP, B, C4, SIM, S, D, DTZ, ERA, PL, PT, Q, RET, TCH, TID, RUF)
- **mypy**: Static type checking with reasonable defaults
- **pytest**: Auto-discovery, parallel execution, timeout protection, coverage enforcement
- **coverage**: Branch coverage, 80% minimum, HTML reports
- **interrogate**: Docstring coverage checking (80% minimum)
- **commitizen**: Conventional commits and semantic versioning

## Development Environment

### VS Code
The project includes VS Code settings in `.vscode/settings.json` for consistent development:
- Ruff formatter integration
- Python testing configuration
- File exclusions for build artifacts

### Dev Container
For containerized development, use the included `.devcontainer/devcontainer.json`:
```bash
# Open in VS Code with Dev Containers extension
code .
# Or use GitHub Codespaces
```

The dev container includes:
- Python 3.14
- Poetry pre-installed
- All recommended VS Code extensions
- Automatic dependency installation

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Ensure tests pass: `make test`
4. Ensure linting passes: `make lint`
5. Format your code: `make format`
6. Commit your changes (pre-commit hooks will run automatically)
7. Push to your branch and create a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
