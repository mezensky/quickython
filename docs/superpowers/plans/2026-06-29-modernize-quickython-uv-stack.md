# quickython uv-Stack Modernization — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate the `quickython` template from Poetry to the modern Astral/uv stack — PEP 621 + hatchling + uv, strict mypy with shipped types, nox task runner, Trusted-Publishing release — and enrich the by-example sample code.

**Architecture:** Single coherent template refresh. The toolchain foundation (uv + `pyproject.toml`) lands first so every later task can use `uv run`. Sample code is built test-first. Config files (nox, CI, pre-commit, docs) follow, each verified by running the real tool and reading its output. Each task ends in a conventional-commit.

**Tech Stack:** Python 3.12–3.14, uv, hatchling, Ruff, mypy (strict), pytest (+cov/xdist/timeout/mock), Hypothesis, interrogate, vulture, pip-audit, commitizen, nox, GitHub Actions, PyPI Trusted Publishing.

> **Note on TDD for config:** Real code (samples) uses strict test-first TDD. Config/tooling changes can't be unit-tested, so their "test" is running the actual tool and confirming the expected output — those steps are written as `Run:` / `Expected:` pairs and must be treated with the same rigor as a failing/passing test.

---

## File Structure

**Created:**
- `src/quickython/example.py` — idiomatic typed sample (frozen dataclass + function).
- `src/quickython/__main__.py` — argparse CLI + `main()` entry point.
- `src/quickython/py.typed` — PEP 561 marker.
- `tests/test_example.py` — parametrize / fixture / mock examples.
- `tests/test_cli.py` — CLI tests.
- `noxfile.py` — task runner sessions.
- `.python-version` — pinned dev interpreter.
- `.github/workflows/release.yml` — Trusted-Publishing release.
- `CONTRIBUTING.md`, `SECURITY.md`, `.github/PULL_REQUEST_TEMPLATE.md` — health files.
- `uv.lock` — generated lockfile.

**Modified:**
- `pyproject.toml` — full PEP 621 rewrite.
- `src/quickython/__init__.py` — version single-sourcing + public exports.
- `tests/test_sample.py` — strict-typed fixtures.
- `.pre-commit-config.yaml`, `.vscode/settings.json`, `.devcontainer/devcontainer.json`, `.gitignore`.
- `.github/workflows/ci.yml`, `.github/dependabot.yml`.
- `CLAUDE.md`, `README.md`, `CHANGELOG.md`.

**Deleted:**
- `Makefile`, `poetry.lock`, `BEST_PRACTICES_ANALYSIS.md`, `IMPLEMENTATION_SUMMARY.md`.

---

## Task 0: Verify prerequisites

- [ ] **Step 1: Confirm uv is installed**

Run: `uv --version`
Expected: prints a version (e.g. `uv 0.x.y`). If "command not found", install it:
`curl -LsSf https://astral.sh/uv/install.sh | sh` (then restart the shell or `source $HOME/.local/bin/env`), or `brew install uv`. Re-run `uv --version` to confirm.

- [ ] **Step 2: Confirm you are on a clean branch at repo root**

Run: `git status --short && pwd`
Expected: working tree clean (the design/plan docs may be committed already), cwd is `.../quickython-mez`.

---

## Task 1: uv + pyproject foundation

**Files:**
- Modify: `pyproject.toml` (full replace)
- Create: `src/quickython/py.typed`
- Create: `.python-version`
- Modify: `.gitignore`
- Delete: `poetry.lock`

- [ ] **Step 1: Replace `pyproject.toml` with the PEP 621 / hatchling / uv version**

Write `pyproject.toml` with exactly this content:

```toml
[project]
name = "quickython"
version = "0.1.0"
description = "Python quick start project template"
readme = "README.md"
requires-python = ">=3.12"
license = "MIT"
authors = [{ name = "Your Name", email = "you@example.com" }]
keywords = ["template", "quickstart", "boilerplate"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    "Typing :: Typed",
]
dependencies = []

[project.urls]
Homepage = "https://github.com/your-org/quickython"
Repository = "https://github.com/your-org/quickython"
Changelog = "https://github.com/your-org/quickython/blob/main/CHANGELOG.md"

[project.scripts]
quickython = "quickython.__main__:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/quickython"]

[dependency-groups]
dev = [
    "ruff",
    "mypy",
    "pytest",
    "pytest-cov",
    "pytest-xdist",
    "pytest-timeout",
    "pytest-mock",
    "hypothesis",
    "interrogate",
    "vulture",
    "pip-audit",
    "commitizen",
    "pre-commit",
    "nox",
]

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "SIM", # flake8-simplify
    "S",   # flake8-bandit (security)
    "D",   # pydocstyle (docstrings)
    "DTZ", # flake8-datetimez
    "ERA", # eradicate (commented-out code)
    "PL",  # pylint
    "PT",  # flake8-pytest-style
    "Q",   # flake8-quotes
    "RET", # flake8-return
    "TCH", # flake8-type-checking
    "TID", # flake8-tidy-imports
    "RUF", # Ruff-specific rules
]
ignore = [
    "S101",    # Use of assert detected (common in tests)
    "D100",    # Missing docstring in public module
    "D104",    # Missing docstring in public package
    "D203",    # 1 blank line before class docstring (conflicts with D211)
    "D213",    # Multi-line docstring summary on second line (conflicts with D212)
    "PLR0913", # Too many arguments to function call
]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["PLR2004"] # magic-value comparisons are fine in tests

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"

[tool.mypy]
python_version = "3.12"
strict = true
files = ["src", "tests"]
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
    "--cov=quickython",
    "--cov-report=term-missing",
    "--cov-branch",
    "--timeout=60",
]

[tool.coverage.run]
source = ["src"]
branch = true
omit = ["*/__pycache__/*"]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
fail_under = 80.0
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if TYPE_CHECKING:",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]

[tool.interrogate]
ignore-init-method = true
ignore-init-module = true
ignore-magic = true
ignore-module = true
ignore-nested-functions = true
fail-under = 80
exclude = ["tests", "docs", ".venv"]
verbose = 2
color = true

[tool.commitizen]
name = "cz_conventional_commits"
version_provider = "pep621"
tag_format = "v$version"
update_changelog_on_bump = true
major_version_zero = true
```

- [ ] **Step 2: Create the `py.typed` marker**

Create `src/quickython/py.typed` as an empty file:

```text
```

(Zero bytes is fine; the file's presence is what matters.)

- [ ] **Step 3: Pin the dev interpreter**

Create `.python-version` with exactly:

```text
3.14
```

- [ ] **Step 4: Update `.gitignore` so `.python-version` and `uv.lock` are tracked**

In `.gitignore`, delete the line `.python-version` (under the `# pyenv` comment) and delete the three-line block:

```text
# Generated requirements files (use poetry export)
requirements.txt
requirements-dev.txt
```

(Do not add `uv.lock` anywhere — it must be committed.)

- [ ] **Step 5: Generate the environment and lockfile**

Run: `uv sync`
Expected: uv creates `.venv/`, resolves dependencies, writes `uv.lock`, and installs the project. Ends with a summary like `Installed N packages`. No errors.

- [ ] **Step 6: Verify the package imports and the baseline tests still pass**

Run: `uv run python -c "import quickython; print('ok')"`
Expected: prints `ok`.

Run: `uv run pytest`
Expected: the existing tests pass (sample + hypothesis), coverage reported. (Strict-typing cleanup happens in later tasks; this only confirms the env works.)

- [ ] **Step 7: Remove the Poetry lockfile**

Run: `git rm poetry.lock`
Expected: `rm 'poetry.lock'`.

- [ ] **Step 8: Commit**

```bash
git add pyproject.toml uv.lock .python-version .gitignore src/quickython/py.typed
git commit -m "build: migrate to uv + PEP 621 + hatchling"
```

---

## Task 2: Idiomatic sample module (`example.py`) — TDD

**Files:**
- Create: `tests/test_example.py`
- Create: `src/quickython/example.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_example.py`:

```python
"""Tests for the example module: fixtures, parametrize, and mocking."""

import pytest
from pytest_mock import MockerFixture

from quickython import example
from quickython.example import Greeting, greet


@pytest.fixture
def default_greeting() -> Greeting:
    """A reusable Greeting fixture."""
    return Greeting(recipient="World")


def test_greeting_render(default_greeting: Greeting) -> None:
    """A Greeting renders as 'salutation, recipient!'."""
    assert default_greeting.render() == "Hello, World!"


def test_greeting_is_frozen(default_greeting: Greeting) -> None:
    """Greeting instances are immutable."""
    with pytest.raises(AttributeError):
        setattr(default_greeting, "recipient", "Mars")


@pytest.mark.parametrize(
    ("name", "salutation", "expected"),
    [
        ("World", "Hello", "Hello, World!"),
        ("  Ada ", "Hi", "Hi, Ada!"),
        ("Bob", "Hey", "Hey, Bob!"),
    ],
)
def test_greet_variants(name: str, salutation: str, expected: str) -> None:
    """greet() trims whitespace and applies the salutation."""
    assert greet(name, salutation=salutation) == expected


@pytest.mark.parametrize("bad", ["", "   ", "\t\n"])
def test_greet_rejects_empty(bad: str) -> None:
    """greet() raises ValueError on empty/whitespace names."""
    with pytest.raises(ValueError, match="must not be empty"):
        greet(bad)


def test_greet_delegates_to_render(mocker: MockerFixture) -> None:
    """greet() builds a Greeting and calls its render() (mock/spy example)."""
    spy = mocker.spy(example.Greeting, "render")
    greet("World")
    spy.assert_called_once()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_example.py -q`
Expected: collection/import error — `ModuleNotFoundError: No module named 'quickython.example'` (or `ImportError` for `Greeting`/`greet`).

- [ ] **Step 3: Implement `example.py`**

Create `src/quickython/example.py`:

```python
"""Idiomatic, fully typed examples to copy from.

Demonstrates a frozen dataclass and a typed function with Google-style
docstrings. Replace these with your own domain code.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Greeting:
    """An immutable greeting addressed to someone.

    Attributes:
        recipient: The name of the person being greeted.
        salutation: The greeting word to use.
    """

    recipient: str
    salutation: str = "Hello"

    def render(self) -> str:
        """Return the greeting as a display string.

        Returns:
            The formatted greeting, e.g. ``"Hello, World!"``.
        """
        return f"{self.salutation}, {self.recipient}!"


def greet(name: str, *, salutation: str = "Hello") -> str:
    """Build a greeting string for ``name``.

    Args:
        name: The recipient's name; surrounding whitespace is stripped.
        salutation: The greeting word to use.

    Returns:
        The rendered greeting.

    Raises:
        ValueError: If ``name`` is empty or only whitespace.
    """
    cleaned = name.strip()
    if not cleaned:
        raise ValueError("name must not be empty")
    return Greeting(recipient=cleaned, salutation=salutation).render()
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `uv run pytest tests/test_example.py -q`
Expected: all tests pass.

- [ ] **Step 5: Lint and type-check the new code**

Run: `uv run ruff check src/quickython/example.py tests/test_example.py`
Expected: `All checks passed!` (if anything is fixable, run `uv run ruff check --fix ...` then re-run).

Run: `uv run ruff format src/quickython/example.py tests/test_example.py`
Expected: files left formatted (reports "N files left unchanged" or reformats them).

Run: `uv run mypy src/quickython/example.py tests/test_example.py`
Expected: `Success: no issues found`.

- [ ] **Step 6: Commit**

```bash
git add src/quickython/example.py tests/test_example.py
git commit -m "feat: add typed dataclass + greet() sample with tests"
```

---

## Task 3: CLI entry point (`__main__.py`) — TDD

**Files:**
- Create: `tests/test_cli.py`
- Create: `src/quickython/__main__.py`

(The `[project.scripts]` entry point was already declared in Task 1.)

- [ ] **Step 1: Write the failing tests**

Create `tests/test_cli.py`:

```python
"""Tests for the command-line interface."""

import pytest

from quickython.__main__ import main


def test_main_default(capsys: pytest.CaptureFixture[str]) -> None:
    """No args greets the world and exits 0."""
    exit_code = main([])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "Hello, World!\n"


def test_main_with_name_and_salutation(capsys: pytest.CaptureFixture[str]) -> None:
    """A positional name and --salutation are used in the greeting."""
    exit_code = main(["Ada", "--salutation", "Hi"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "Hi, Ada!\n"


def test_main_empty_name_errors(capsys: pytest.CaptureFixture[str]) -> None:
    """An empty name triggers argparse's usage error (exit code 2)."""
    with pytest.raises(SystemExit) as excinfo:
        main(["   "])
    assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert "must not be empty" in captured.err
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_cli.py -q`
Expected: `ModuleNotFoundError: No module named 'quickython.__main__'`.

- [ ] **Step 3: Implement `__main__.py`**

Create `src/quickython/__main__.py`:

```python
"""Command-line entry point for quickython.

Run with ``python -m quickython`` or the installed ``quickython`` script.
Uses the stdlib ``argparse`` to stay dependency-free; swap in Typer or Click
here if you want a richer CLI.
"""

import argparse
from collections.abc import Sequence

from quickython.example import greet


def build_parser() -> argparse.ArgumentParser:
    """Construct the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="quickython",
        description="Print a greeting (sample CLI).",
    )
    parser.add_argument("name", nargs="?", default="World", help="Who to greet.")
    parser.add_argument(
        "-s",
        "--salutation",
        default="Hello",
        help="Greeting word to use (default: %(default)s).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI.

    Args:
        argv: Argument list (defaults to ``sys.argv[1:]`` when ``None``).

    Returns:
        Process exit code (``0`` on success).
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        print(greet(args.name, salutation=args.salutation))
    except ValueError as exc:
        parser.error(str(exc))  # raises SystemExit(2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `uv run pytest tests/test_cli.py -q`
Expected: all three tests pass.

- [ ] **Step 5: Verify the installed console script and module form work**

Run: `uv run quickython Ada --salutation Hi`
Expected: prints `Hi, Ada!`

Run: `uv run python -m quickython`
Expected: prints `Hello, World!`

- [ ] **Step 6: Lint and type-check**

Run: `uv run ruff check src/quickython/__main__.py tests/test_cli.py`
Expected: `All checks passed!`

Run: `uv run mypy src/quickython/__main__.py tests/test_cli.py`
Expected: `Success: no issues found`.

- [ ] **Step 7: Commit**

```bash
git add src/quickython/__main__.py tests/test_cli.py
git commit -m "feat: add argparse CLI entry point with tests"
```

---

## Task 4: Public API + version single-sourcing (`__init__.py`), tidy `test_sample.py`

**Files:**
- Modify: `src/quickython/__init__.py`
- Modify: `tests/test_sample.py`

- [ ] **Step 1: Rewrite `__init__.py`**

Replace `src/quickython/__init__.py` with:

```python
"""quickython - A quick start Python project template."""

from importlib.metadata import PackageNotFoundError, version

from quickython.example import Greeting, greet
from quickython.sample import samplefunction

try:
    __version__ = version("quickython")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"

__all__ = ["Greeting", "__version__", "greet", "samplefunction"]
```

- [ ] **Step 2: Update `tests/test_sample.py` to strict-typed fixtures**

Replace `tests/test_sample.py` with:

```python
"""Tests for the sample module."""

import pytest

from quickython.sample import samplefunction


def test_samplefunction_prints_hey(capsys: pytest.CaptureFixture[str]) -> None:
    """samplefunction prints 'Hey' to stdout."""
    samplefunction()
    captured = capsys.readouterr()
    assert captured.out == "Hey\n"


def test_samplefunction_returns_none() -> None:
    """samplefunction returns None."""
    assert samplefunction() is None  # type: ignore[func-returns-value]


def test_samplefunction_called_multiple_times(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """samplefunction can be called repeatedly."""
    samplefunction()
    samplefunction()
    captured = capsys.readouterr()
    assert captured.out == "Hey\nHey\n"
```

- [ ] **Step 3: Verify version single-sourcing**

Run: `uv run python -c "import quickython; print(quickython.__version__)"`
Expected: prints `0.1.0` (sourced from `[project].version` via `importlib.metadata`).

- [ ] **Step 4: Lint (incl. `__all__` sort) and type-check the whole tree**

Run: `uv run ruff check --fix src tests`
Expected: `All checks passed!` (the `--fix` normalizes `__all__` ordering via RUF022 if needed).

Run: `uv run ruff format src tests`
Expected: files formatted / unchanged.

Run: `uv run mypy`
Expected: `Success: no issues found in N source files`.

- [ ] **Step 5: Run the full suite with coverage gate**

Run: `uv run pytest -n auto --cov-fail-under=80`
Expected: all tests pass; total coverage ≥ 80%.

- [ ] **Step 6: Commit**

```bash
git add src/quickython/__init__.py tests/test_sample.py
git commit -m "refactor: single-source __version__ and export public API"
```

---

## Task 5: nox task runner (replace the Makefile)

**Files:**
- Create: `noxfile.py`
- Delete: `Makefile`

- [ ] **Step 1: Create `noxfile.py`**

```python
"""Developer task automation via nox (uv-backed).

List sessions with ``uv run nox -l`` and run one with ``uv run nox -s <name>``.
Every tool is also runnable directly, e.g. ``uv run pytest`` or ``uv run mypy``.
"""

import nox

nox.options.default_venv_backend = "uv"
nox.options.sessions = ["lint", "type_check", "tests"]

PYTHON_VERSIONS = ["3.12", "3.13", "3.14"]
DEFAULT_PYTHON = "3.14"
LINT_TARGETS = ["src", "tests", "noxfile.py"]


def _sync(session: nox.Session) -> None:
    """Install the project + dev dependencies into the session venv via uv."""
    session.run_install(
        "uv",
        "sync",
        "--frozen",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )


@nox.session(python=DEFAULT_PYTHON)
def lint(session: nox.Session) -> None:
    """Run Ruff lint and format checks."""
    _sync(session)
    session.run("ruff", "check", *LINT_TARGETS)
    session.run("ruff", "format", "--check", *LINT_TARGETS)


@nox.session(python=DEFAULT_PYTHON)
def format(session: nox.Session) -> None:  # noqa: A001 - nox session name
    """Auto-fix lint issues and format the code."""
    _sync(session)
    session.run("ruff", "check", "--fix", *LINT_TARGETS)
    session.run("ruff", "format", *LINT_TARGETS)


@nox.session(name="type_check", python=DEFAULT_PYTHON)
def type_check(session: nox.Session) -> None:
    """Run mypy in strict mode."""
    _sync(session)
    session.run("mypy")


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """Run the test suite with coverage on each supported Python."""
    _sync(session)
    session.run(
        "pytest",
        "-n",
        "auto",
        "--cov-report=xml",
        "--cov-fail-under=80",
        *session.posargs,
    )


@nox.session(python=DEFAULT_PYTHON)
def coverage(session: nox.Session) -> None:
    """Run tests and emit an HTML coverage report under htmlcov/."""
    _sync(session)
    session.run("pytest", "--cov-report=html", "--cov-report=term")


@nox.session(python=DEFAULT_PYTHON)
def security(session: nox.Session) -> None:
    """Audit installed dependencies for known vulnerabilities."""
    _sync(session)
    session.run("pip-audit")


@nox.session(python=DEFAULT_PYTHON)
def docstrings(session: nox.Session) -> None:
    """Check docstring coverage."""
    _sync(session)
    session.run("interrogate", "-v", "src")


@nox.session(name="dead_code", python=DEFAULT_PYTHON)
def dead_code(session: nox.Session) -> None:
    """Detect unused / dead code."""
    _sync(session)
    session.run("vulture", "src", "--min-confidence", "80")


@nox.session(python=DEFAULT_PYTHON)
def build(session: nox.Session) -> None:
    """Build the sdist and wheel with uv."""
    session.run("uv", "build", external=True)
```

- [ ] **Step 2: Delete the Makefile**

Run: `git rm Makefile`
Expected: `rm 'Makefile'`.

- [ ] **Step 3: Verify nox discovers all sessions**

Run: `uv run nox -l`
Expected: lists `lint`, `format`, `type_check`, `tests-3.12`, `tests-3.13`, `tests-3.14`, `coverage`, `security`, `docstrings`, `dead_code`, `build` (the first three marked as the default selection).

- [ ] **Step 4: Run the default sessions end-to-end**

Run: `uv run nox -s lint type_check`
Expected: both sessions create uv-backed venvs and pass (`ruff` checks pass, mypy `Success`). Session summary shows `* lint: success` and `* type_check: success`.

Run: `uv run nox -s tests-3.14`
Expected: nox provisions Python 3.14 via uv, installs deps, runs pytest; tests pass, coverage ≥ 80%, `* tests-3.14: success`.

> If `tests-3.12`/`tests-3.13` are run and the interpreter is missing, uv downloads it automatically; allow extra time on first run.

- [ ] **Step 5: Commit**

```bash
git add noxfile.py
git commit -m "build: add nox task runner, remove Makefile"
```

---

## Task 6: pre-commit, VS Code, and dev container

**Files:**
- Modify: `.pre-commit-config.yaml`
- Modify: `.vscode/settings.json`
- Modify: `.devcontainer/devcontainer.json`

- [ ] **Step 1: Rewrite `.pre-commit-config.yaml`**

Replace its contents with:

```yaml
default_install_hook_types: [pre-commit, pre-push]
default_stages: [pre-commit]

repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: check-toml
      - id: debug-statements
      - id: mixed-line-ending

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.5
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # mypy and pytest run in the project env (full deps + strict config) via uv.
  - repo: local
    hooks:
      - id: mypy
        name: mypy
        entry: uv run mypy
        language: system
        types: [python]
        pass_filenames: false
        require_serial: true

      - id: pytest
        name: pytest (pre-push)
        entry: uv run pytest --cov-fail-under=80
        language: system
        pass_filenames: false
        always_run: true
        stages: [pre-push]
```

- [ ] **Step 2: Bump the hook revisions to latest**

Run: `uv run pre-commit autoupdate`
Expected: updates the `rev:` values for `pre-commit-hooks` and `ruff-pre-commit` to their latest tags (prints `updating ... -> ...`). The two `local` hooks are unaffected.

- [ ] **Step 3: Install the hooks and run them against all files**

Run: `uv run pre-commit install --install-hooks`
Expected: `pre-commit installed at .git/hooks/pre-commit` and `...pre-push`.

Run: `uv run pre-commit run --all-files`
Expected: every hook passes. (If a formatting/whitespace hook auto-modifies a file, re-stage with `git add -A` and re-run until all hooks report `Passed`.)

- [ ] **Step 4: Update `.vscode/settings.json` (remove the deprecated linting flag)**

In `.vscode/settings.json`, delete these two lines:

```json
  // Linting - Using ruff via CLI
  "python.linting.enabled": false,
```

Leave the rest of the file unchanged.

- [ ] **Step 5: Update `.devcontainer/devcontainer.json` to use uv**

Replace its contents with:

```json
{
  "name": "quickython",
  "image": "mcr.microsoft.com/devcontainers/python:3.14",

  "features": {
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/common-utils:2": {
      "installZsh": true,
      "installOhMyZsh": true
    }
  },

  "postCreateCommand": "pip install uv && uv sync",

  "customizations": {
    "vscode": {
      "extensions": [
        "charliermarsh.ruff",
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.mypy-type-checker",
        "tamasfe.even-better-toml"
      ],
      "settings": {
        "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
        "python.testing.pytestEnabled": true,
        "editor.formatOnSave": true,
        "[python]": {
          "editor.defaultFormatter": "charliermarsh.ruff"
        }
      }
    }
  },

  "forwardPorts": [],

  "remoteUser": "vscode"
}
```

- [ ] **Step 6: Validate the dev container JSON parses**

Run: `uv run python -c "import json; json.load(open('.devcontainer/devcontainer.json')); print('json ok')"`
Expected: prints `json ok`.

> Note: do **not** `json.load` `.vscode/settings.json` — it is JSONC (the `//`
> comments are valid there) and would raise `JSONDecodeError`. Verify it by eye:
> confirm only the two specified lines were removed and the braces/commas are intact.

- [ ] **Step 7: Commit**

```bash
git add .pre-commit-config.yaml .vscode/settings.json .devcontainer/devcontainer.json
git commit -m "build: modernize pre-commit, VS Code, and dev container for uv"
```

---

## Task 7: CI, release, and Dependabot

**Files:**
- Modify: `.github/workflows/ci.yml`
- Create: `.github/workflows/release.yml`
- Modify: `.github/dependabot.yml`

- [ ] **Step 1: Rewrite `.github/workflows/ci.yml`**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  quality:
    name: Lint & type-check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true
      - name: Lint and type-check
        run: uvx nox -s lint type_check

  tests:
    name: Tests (py${{ matrix.python-version }})
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.12", "3.13", "3.14"]
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true
      - name: Run tests
        run: uvx nox --python ${{ matrix.python-version }} -s tests
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v5
        with:
          files: ./coverage.xml
          fail_ci_if_error: false
        env:
          CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

- [ ] **Step 2: Create `.github/workflows/release.yml`**

```yaml
name: Release

on:
  push:
    tags: ["v*"]

jobs:
  build:
    name: Build distributions
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        uses: astral-sh/setup-uv@v5
      - name: Build sdist and wheel
        run: uv build
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  publish:
    name: Publish to PyPI (Trusted Publishing)
    needs: build
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      - name: Publish
        uses: pypa/gh-action-pypi-publish@release/v1
```

- [ ] **Step 3: Rewrite `.github/dependabot.yml`**

```yaml
version: 2
updates:
  - package-ecosystem: "uv"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "python"
    commit-message:
      prefix: "deps"
      include: "scope"
    groups:
      dev-dependencies:
        patterns: ["*"]
        update-types: ["minor", "patch"]

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    labels:
      - "dependencies"
      - "github-actions"
    commit-message:
      prefix: "ci"
    groups:
      actions:
        patterns: ["*"]
```

- [ ] **Step 4: Validate the workflow/Dependabot YAML parses**

Run: `uv run python -c "import yaml,glob; [yaml.safe_load(open(p)) for p in glob.glob('.github/**/*.yml', recursive=True)]; print('yaml ok')"`
Expected: prints `yaml ok`. (PyYAML is available transitively via the dev env; if it is not, run `uvx --with pyyaml python -c "..."` with the same body.)

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/ci.yml .github/workflows/release.yml .github/dependabot.yml
git commit -m "ci: uv-based CI, Trusted-Publishing release, uv Dependabot"
```

---

## Task 8: Documentation & community-health files

**Files:**
- Delete: `BEST_PRACTICES_ANALYSIS.md`, `IMPLEMENTATION_SUMMARY.md`
- Modify: `CLAUDE.md`, `README.md`, `CHANGELOG.md`
- Create: `CONTRIBUTING.md`, `SECURITY.md`, `.github/PULL_REQUEST_TEMPLATE.md`

- [ ] **Step 1: Delete the build-history meta-docs**

Run: `git rm BEST_PRACTICES_ANALYSIS.md IMPLEMENTATION_SUMMARY.md`
Expected: both files removed.

- [ ] **Step 2: Rewrite `CLAUDE.md` as a lean conventions doc**

Replace `CLAUDE.md` with:

```markdown
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
- One task: `uv run nox -s lint` / `type_check` / `tests` / `coverage` /
  `security` / `docstrings` / `dead_code` / `build`
- Ad-hoc: `uv run pytest`, `uv run ruff check`, `uv run mypy`
- Run the sample CLI: `uv run quickython --help`

## Conventions

- Python ≥ 3.12; code targets py312 (Ruff/mypy). Keep `requires-python`, the CI
  matrix, and the Ruff/mypy targets in sync if you change the floor.
- New code is fully typed and passes `mypy --strict`. Public API is exported via
  `__all__` in `__init__.py`; `__version__` is sourced from package metadata.
- Quality gates: ≥ 80% test coverage, ≥ 80% docstring coverage (interrogate).
- Commit messages follow Conventional Commits (commitizen); bump with `cz bump`.

## Using this template for an app (not a library)

Drop the publishing bits: remove `[project.scripts]` if unused,
`.github/workflows/release.yml`, and the `build` nox session; you can keep
everything else as-is.
```

- [ ] **Step 3: Rewrite `README.md`**

Replace `README.md` with:

````markdown
# quickython

A production-ready **quick-start template** for new Python projects, built on the
modern Astral/uv toolchain with opinionated quality defaults.

## What's inside

- **uv** for environments, dependencies, and builds (PEP 621 + hatchling).
- **Ruff** (lint + format) and **mypy** in **strict** mode; the package ships
  `py.typed` so consumers get your types.
- **pytest** with coverage (≥ 80% gate), parallel runs (xdist), timeouts, mocking,
  and **Hypothesis** property-based tests.
- **nox** task runner, **pre-commit** hooks, **commitizen** for Conventional
  Commits + versioning.
- GitHub Actions CI across Python 3.12–3.14 and a **PyPI Trusted Publishing**
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

## Using this as an app starter

Not shipping to PyPI? Delete `.github/workflows/release.yml`, the `build` nox
session, and (if unused) `[project.scripts]`. Everything else applies unchanged.

## License

MIT — see [LICENSE](LICENSE).
````

- [ ] **Step 4: Add a CHANGELOG entry under the existing `## [Unreleased]`**

The file already has an `## [Unreleased]` header (followed by `### Added (2026-02-06) ...`). Do **not** add a second `## [Unreleased]`. Insert this block on the line **immediately after** `## [Unreleased]` and **before** `### Added (2026-02-06) - Comprehensive Best Practices Implementation`, matching the file's dated-subsection style:

```markdown
### Changed (2026-06-29) - Migrated to the uv Toolchain

#### Tooling
- Migrated from Poetry to **uv** with PEP 621 metadata and the **hatchling**
  build backend; `uv.lock` replaces `poetry.lock`.
- Enabled **mypy strict** mode and shipped a `py.typed` marker (PEP 561).
- Replaced the Makefile with a **nox** task runner.
- Rebuilt CI on uv (Python 3.12–3.14); releases now use **PyPI Trusted
  Publishing** (OIDC) instead of twine + tokens.
- `__version__` is now single-sourced from package metadata.

#### Added
- Idiomatic samples: a typed frozen dataclass, a `greet()` function, and an
  `argparse` CLI entry point, with parametrize/fixture/mock test examples.
- `CONTRIBUTING.md`, `SECURITY.md`, and a pull-request template.

#### Removed
- Poetry, twine, and the build-history meta-docs
  (`BEST_PRACTICES_ANALYSIS.md`, `IMPLEMENTATION_SUMMARY.md`).

```

- [ ] **Step 5: Create `CONTRIBUTING.md`**

````markdown
# Contributing

Thanks for contributing! This project uses the uv toolchain.

## Setup

```bash
uv sync
uv run pre-commit install --install-hooks
```

## Workflow

1. Create a branch.
2. Make your change with tests. Keep the code fully typed.
3. Run the gates locally:
   ```bash
   uv run nox          # lint + type_check + tests
   ```
4. Commit using [Conventional Commits](https://www.conventionalcommits.org/)
   (e.g. `feat: ...`, `fix: ...`). `commitizen` enforces this; `uv run cz commit`
   can guide you.
5. Open a pull request and fill in the template.

## Standards

- `mypy --strict` must pass; new code is fully type-annotated.
- Test coverage stays at or above 80%.
- Public docstrings follow the Google convention.
````

- [ ] **Step 6: Create `SECURITY.md`**

```markdown
# Security Policy

## Supported versions

This is a project template; the latest `main` is supported.

## Reporting a vulnerability

Please report security issues privately via GitHub's **Report a vulnerability**
(Security tab) or by emailing the maintainer listed in `pyproject.toml`. Do not
open a public issue for security reports. We aim to acknowledge reports within a
few business days.
```

- [ ] **Step 7: Create `.github/PULL_REQUEST_TEMPLATE.md`**

```markdown
## Summary

<!-- What does this change and why? -->

## Checklist

- [ ] Tests added/updated and passing (`uv run nox -s tests`)
- [ ] `uv run nox -s lint type_check` passes
- [ ] Coverage ≥ 80%
- [ ] Conventional Commit message(s)
- [ ] Docs/CHANGELOG updated if needed
```

- [ ] **Step 8: Re-run hooks over the new docs and commit**

Run: `uv run pre-commit run --all-files`
Expected: all hooks pass (re-stage and re-run if a whitespace/EOF hook adjusts a file).

```bash
git add CLAUDE.md README.md CHANGELOG.md CONTRIBUTING.md SECURITY.md .github/PULL_REQUEST_TEMPLATE.md
git commit -m "docs: rewrite for uv stack and add community-health files"
```

---

## Task 9: Final acceptance verification

**Files:** none (verification only)

- [ ] **Step 1: Full quality gate across all Pythons**

Run: `uv run nox`
Expected: `lint`, `type_check`, and `tests-3.12/3.13/3.14` all succeed. Final summary lists every session as `success`.

- [ ] **Step 2: Extended gates**

Run: `uv run nox -s docstrings dead_code security`
Expected: interrogate ≥ 80% (`RESULT: PASSED`), vulture reports no high-confidence dead code, pip-audit finds no known vulnerabilities (`No known vulnerabilities found`).

- [ ] **Step 3: Build and confirm the wheel ships `py.typed`**

Run: `uv build`
Expected: writes `dist/quickython-0.1.0.tar.gz` and `dist/quickython-0.1.0-py3-none-any.whl`.

Run: `uv run python -c "import zipfile,glob; w=glob.glob('dist/*.whl')[0]; names=zipfile.ZipFile(w).namelist(); assert 'quickython/py.typed' in names, names; print('py.typed shipped in', w)"`
Expected: prints `py.typed shipped in dist/...whl` (assertion passes).

- [ ] **Step 4: Confirm no stale Poetry references remain**

Run: `grep -rn -i --include=*.toml --include=*.yml --include=*.yaml --include=*.json --include=*.cfg --include=*.ini --include=Makefile --include=*.py --exclude-dir=.git --exclude-dir=.venv --exclude-dir=docs "poetry" . || echo "no poetry references"`
Expected: `no poetry references`. (Scoped to config/code files — `*.md` docs like the CHANGELOG legitimately mention Poetry in their migration notes and are excluded. If any real config hit appears, fix it.)

- [ ] **Step 5: Confirm version consistency**

Run: `uv run python -c "import quickython; print(quickython.__version__)"`
Expected: `0.1.0` (matches `[project].version`).

- [ ] **Step 6: Confirm the dist artifacts are not committed**

Run: `git status --short`
Expected: `dist/` (and `.venv/`, caches) are untracked/ignored — not staged. The only tracked changes should already be committed from prior tasks.

- [ ] **Step 7: Final sanity commit (if anything is pending)**

If `git status` shows tracked changes (e.g. a lock refresh), commit them:

```bash
git add -A
git commit -m "chore: finalize uv-stack modernization"
```

Otherwise, the migration is complete.

---

## Self-Review Notes (for the implementer)

- **Strict mypy on tests:** if a decorator (`@given`, `@pytest.mark.parametrize`)
  ever trips `disallow_untyped_decorators`, the libraries are typed and ship
  `py.typed`, so a clean `uv sync` resolves it; only add a narrow
  `# type: ignore[misc]` as a last resort.
- **Tool versions are intentionally unpinned** in `[dependency-groups]`; `uv.lock`
  provides reproducibility. Do not add floors unless a real incompatibility appears.
- **First nox run is slow** while uv downloads 3.12/3.13 interpreters — expected.
- **GitHub Action major versions** (`setup-uv@v5`, `codecov-action@v5`) are pinned
  to known-good majors; Dependabot's `github-actions` updater will bump them.
