# CLAUDE.md

Project context for working in **quickython** — a copy-and-go template for new
Python projects using the modern Astral/uv toolchain.

## Stack

- **uv** — environment, dependency, and build management. `uv.lock` is committed.
- **hatchling** — PEP 517 build backend; metadata is PEP 621 (`[project]`).
- **Ruff** — lint + format. **mypy** — strict type checking. The package ships
  `py.typed`.
- **pytest** (+cov, xdist, timeout, mock) and **Hypothesis** for tests.
- **nox** — task runner. **commitizen** — conventional commits + versioning.
- CI on GitHub Actions; releases publish to PyPI via Trusted Publishing.

## Layout

- `src/quickython/` — package code (`sample.py`, `example.py`, `__main__.py`).
- `tests/` — mirrors the package; see the existing files for the test idioms
  (capsys, parametrize, fixtures, mocker, Hypothesis).
- `noxfile.py` — all dev tasks. `pyproject.toml` — all tool config.

## Common commands

- Install: `uv sync`
- Everything (lint + types + tests): `uv run nox`
- One task: `uv run nox -s lint` / `format` / `type_check` / `tests` /
  `coverage` / `security` / `docstrings` / `dead_code` / `build`
- Ad-hoc: `uv run pytest`, `uv run ruff check`, `uv run mypy`
- Run the sample CLI: `uv run quickython --help`

## Conventions

- Python >= 3.12; code targets py312 (Ruff/mypy). Keep `requires-python`, the CI
  matrix, and the Ruff/mypy targets in sync if you change the floor.
- New code is fully typed and passes `mypy --strict`. Public API is exported via
  `__all__` in `__init__.py`; `__version__` is sourced from package metadata.
- Quality gates: >= 80% test coverage, >= 80% docstring coverage (interrogate).
- Commit messages follow Conventional Commits (commitizen); bump with `cz bump`.

## Using this template for an app (not a library)

Drop the publishing bits: remove `[project.scripts]` if unused,
`.github/workflows/release.yml`, and the `build` nox session; you can keep
everything else as-is.
