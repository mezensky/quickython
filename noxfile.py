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


@nox.session(name="format", python=DEFAULT_PYTHON)
def fmt(session: nox.Session) -> None:
    """Auto-fix lint issues and format the code."""
    _sync(session)
    session.run("ruff", "check", "--fix", *LINT_TARGETS)
    session.run("ruff", "format", *LINT_TARGETS)


@nox.session(name="type_check", python=DEFAULT_PYTHON)
def type_check(session: nox.Session) -> None:
    """Run mypy in strict mode."""
    _sync(session)
    session.run("mypy", *session.posargs)


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """Run the full test suite with XML coverage on each supported Python (CI)."""
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
    """Run tests and emit an HTML coverage report under htmlcov/ (local dev)."""
    _sync(session)
    session.run("pytest", "--cov-report=html")


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
