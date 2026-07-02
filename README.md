# quickython

A production-ready **quick-start template** for new Python projects, built on the
modern Astral/uv toolchain with opinionated quality defaults.

## What's inside

- **uv** for environments, dependencies, and builds (PEP 621 + hatchling).
- **Ruff** (lint + format) and **mypy** in **strict** mode; the package ships
  `py.typed` so consumers get your types.
- **pytest** with coverage (>= 80% gate), parallel runs (xdist), timeouts, mocking,
  and **Hypothesis** property-based tests.
- **nox** task runner, **pre-commit** hooks, **commitizen** for Conventional
  Commits + versioning.
- GitHub Actions CI across Python 3.12-3.14 and a **PyPI Trusted Publishing**
  release workflow (no tokens).
- Sample code demonstrating a typed dataclass, a function, and an `argparse` CLI.

## Requirements

- [uv](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Python 3.12+ (uv can install interpreters for you)

## Quick start

```bash
uv sync                 # create .venv and install everything
uv run nox              # lint + type-check + tests
uv run quickython --help
```

## Common commands

| Task | Command |
| --- | --- |
| Install / update env | `uv sync` |
| Lint + types + tests | `uv run nox` |
| Lint only | `uv run nox -s lint` |
| Auto-format & fix | `uv run nox -s format` |
| Type-check (strict) | `uv run nox -s type_check` |
| Tests (one Python) | `uv run nox -s tests-3.14` |
| HTML coverage | `uv run nox -s coverage` |
| Security audit | `uv run nox -s security` |
| Docstring coverage | `uv run nox -s docstrings` |
| Dead-code scan | `uv run nox -s dead_code` |
| Build sdist + wheel | `uv run nox -s build` |

Any tool also runs directly, e.g. `uv run pytest -k cli` or `uv run ruff check`.

## Project layout

```
quickython/
├── src/quickython/      # package code
│   ├── __init__.py      # public API + __version__ (from metadata)
│   ├── sample.py        # minimal sample function
│   ├── example.py       # typed dataclass + function sample
│   ├── __main__.py      # argparse CLI (also the `quickython` script)
│   └── py.typed         # PEP 561 marker
├── tests/               # pytest + Hypothesis examples
├── noxfile.py           # dev tasks
├── pyproject.toml       # project + tool configuration
└── uv.lock              # locked dependencies (committed)
```

## Releasing (libraries)

Releases use **PyPI Trusted Publishing** — no API tokens.

1. On PyPI, add a trusted publisher for this repo's `release.yml` workflow and a
   GitHub Environment named `pypi` (one-time setup).
2. Bump the version and tag: `uv run cz bump` (creates a `vX.Y.Z` tag).
3. `git push --follow-tags`. The tag triggers `release.yml`, which builds and
   publishes via OIDC.

Coverage upload to Codecov is optional: set a `CODECOV_TOKEN` repository secret to
enable it. CI does not fail if the token is absent.

## Using this as an app starter

Not shipping to PyPI? Delete `.github/workflows/release.yml`, the `build` nox
session, and (if unused) `[project.scripts]`. Everything else applies unchanged.

## License

MIT — see [LICENSE](LICENSE).
