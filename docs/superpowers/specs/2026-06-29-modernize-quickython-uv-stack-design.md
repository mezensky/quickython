# Modernize `quickython` onto the uv / Astral Stack — Design Spec

**Date:** 2026-06-29
**Status:** Approved-pending-review
**Author:** Peter Mezensky (with Claude)

## 1. Goal & Philosophy

`quickython` is a copy-and-go quick-start template for new Python projects. It
should model the toolchain and structure favored by the part of the Python
community that cares about **structure, quality, and opinionated development** —
the "hypermodern Python" lineage — using current (mid-2026) best practices.

This is a refresh of an existing, well-structured but ~1-year-stale template. The
macro decision is to migrate the toolchain from Poetry to the **Astral/uv stack**,
tighten type checking, enrich the by-example samples, and modernize CI/publishing.

### Decisions locked during brainstorming

| Decision | Choice |
|---|---|
| Dependency / env / build manager | **uv** (migrate off Poetry) |
| Type-checking rigor | **mypy strict** + ship `py.typed` (no `ty` preview) |
| Sample code | **Add idiomatic samples** (dataclass, CLI entry point, richer tests) |
| Distribution model | **Library** with **PyPI Trusted Publishing (OIDC)** |
| Task runner | **nox** (replaces the Makefile) |
| Community-health files | **Lean set**: CONTRIBUTING.md, SECURITY.md, PR template |
| Build backend | **hatchling** |
| Version single-sourcing | `[project].version` in pyproject; `__version__` via `importlib.metadata`; commitizen `version_provider = "pep621"` |

## 2. Non-Goals (YAGNI)

- No docs site (mkdocs-material / Sphinx) — out of scope for a quick-start.
- No `ty` (Astral type checker, preview) — revisit when it stabilizes.
- No runtime dependencies added — the CLI sample uses stdlib `argparse`.
- No CODE_OF_CONDUCT / issue templates (lean health set only).
- No dynamic git-tag versioning (hatch-vcs) — noted as a future option, not adopted.

## 3. Python version policy

Resolve the current contradiction (`requires-python = "^3.14"` vs CI testing
3.12/3.13 vs Ruff `target-version = "py313"`):

- `requires-python = ">=3.12"` (library-appropriate range).
- CI test matrix: **3.12, 3.13, 3.14**.
- Ruff `target-version = "py312"`.
- mypy `python_version = "3.12"`.
- `.python-version` committed, pinned to **3.14** (latest, for local dev) — removed from `.gitignore`.

## 4. Packaging & environment (uv + PEP 621)

### `pyproject.toml` rewrite

- Replace `[tool.poetry]` with **PEP 621 `[project]`**:
  - `name`, `version = "0.1.0"`, `description`, `readme`, `requires-python = ">=3.12"`.
  - `authors = [{ name = "Your Name", email = "you@example.com" }]` (placeholder — no corporate email).
  - `license = "MIT"` (PEP 639 SPDX expression, current standard) with `LICENSE` file present.
  - `classifiers` (Python versions, `Typing :: Typed`) — **no** `License :: OSI Approved` classifier, which PEP 639 deprecates when an SPDX expression is used.
  - `[project.urls]` (Homepage / Repository / Changelog) as placeholders.
  - `[project.scripts] quickython = "quickython.__main__:main"`.
- `[build-system]`: `requires = ["hatchling"]`, `build-backend = "hatchling.build"`.
- `[tool.hatch.build.targets.wheel] packages = ["src/quickython"]`, and ensure `py.typed` is included.
- Dev tooling under **PEP 735 `[dependency-groups]`** → `dev` group:
  `ruff`, `mypy`, `pytest`, `pytest-cov`, `pytest-xdist`, `pytest-timeout`,
  `pytest-mock`, `hypothesis`, `interrogate`, `vulture`, `pip-audit`,
  `commitizen`, `pre-commit`, `nox`.
  - Removed from deps: `poetry-core`, `build`, `twine` (build/publish handled by uv + GH Action).
- Keep all existing `[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]`,
  `[tool.coverage.*]`, `[tool.interrogate]`, `[tool.commitizen]` tables, updated per below.

### Lockfile & artifacts

- Generate **`uv.lock`**; commit it; delete `poetry.lock`.
- Remove the `poetry export` / `requirements*.txt` workflow (uv.lock is the source of truth; `uv export` available if needed). Keep the `requirements*.txt` ignore lines harmless or drop them.

## 5. Lint / format / types

- **Ruff**: bump to current (~0.12+). Keep the existing comprehensive `select`
  set; re-validate the `ignore` list against current Ruff (notably keep `S101`,
  `D203`, `D213`; keep `PLR0913`). `target-version = "py312"`. Keep
  `[tool.ruff.format]` (double quotes, magic trailing comma).
- **mypy**: replace the hand-rolled lax flags with `strict = true`. Keep
  `files = ["src", "tests"]`, `python_version = "3.12"`, `warn_unused_configs`,
  `warn_redundant_casts`, `warn_unused_ignores`.
- **PEP 561**: add empty `src/quickython/py.typed`; ensure the wheel ships it.
- Keep `interrogate` (docstring-coverage gate, 80%) and `vulture` (dead code) as
  opinionated quality extras, invoked via nox.

## 6. Testing

- Keep the pytest stack: `pytest`, `pytest-cov`, `pytest-xdist` (`-n auto`),
  `pytest-timeout`, `pytest-mock`, `hypothesis`.
- Keep `[tool.pytest.ini_options]` (`--strict-markers`, `--strict-config`,
  branch coverage, `--timeout=60`) and the **80% coverage gate**.
- Run via nox (`uv`-backed venvs) across the Python matrix.

## 7. Sample code (demonstrate idioms by example)

New/updated `src/` layout:

- `src/quickython/__init__.py` — package docstring; `__version__ =
  importlib.metadata.version("quickython")` (single-source); `__all__` re-exporting
  the public API.
- `src/quickython/sample.py` — keep a cleaned `samplefunction` for continuity.
- `src/quickython/example.py` — idiomatic typed example:
  - a frozen `@dataclass(slots=True)` (e.g. `Greeting`),
  - a fully type-hinted function (e.g. `greet(name: str) -> str`) using modern
    typing (`X | None`, built-in generics), Google-style docstrings.
- `src/quickython/__main__.py` — stdlib `argparse` CLI calling `greet`, exposing
  `main() -> int`; wired to the `quickython` console script. Comment notes how to
  swap in Typer if a richer CLI is wanted (no dep added).
- `src/quickython/py.typed` — marker.

New/updated `tests/`:

- `tests/test_sample.py` — keep/clean (capsys example).
- `tests/test_example.py` — `@pytest.mark.parametrize`, a `fixture`, and a
  `pytest-mock` (`mocker`) example.
- `tests/test_cli.py` — exercise `__main__.main` (argv + capsys), demonstrating
  CLI testing and exit codes.
- `tests/test_hypothesis_example.py` — keep.

## 8. Task runner — nox

- Delete `Makefile`.
- Add `noxfile.py` with `nox.options.default_venv_backend = "uv"` and sessions:
  - `lint` — `ruff check` + `ruff format --check`.
  - `format` — `ruff check --fix` + `ruff format`.
  - `type_check` — `mypy`.
  - `tests` — `@nox.session(python=["3.12","3.13","3.14"])`, runs pytest with coverage.
  - `coverage` — HTML/term report.
  - `security` — `pip-audit`.
  - `docstrings` — `interrogate`.
  - `dead_code` — `vulture`.
  - `build` — `uv build`.
- README documents that `uv run <tool>` also works directly for ad-hoc use.

## 9. CI/CD & publishing

### `.github/workflows/ci.yml` (rewrite)

- Use **`astral-sh/setup-uv`** (with caching) + `actions/checkout`.
- Matrix over Python **3.12 / 3.13 / 3.14**; each job runs `nox -s tests` for its
  interpreter (`nox --python ${{ matrix.python-version }} -s tests`).
- Single-interpreter jobs: `nox -s lint type_check`.
- Codecov upload kept, **non-blocking** (`fail_ci_if_error: false`, token optional).

### `.github/workflows/release.yml` (new)

- Trigger: push of a `v*` tag.
- Build with `uv build`; publish via **`pypa/gh-action-pypi-publish`** using
  **Trusted Publishing (OIDC)** — `permissions: id-token: write`, no tokens/twine.
- Document the one-time PyPI trusted-publisher setup in README.

### `.github/dependabot.yml`

- Switch `package-ecosystem: "pip"` → **`"uv"`**.
- Add `groups` to batch minor/patch dev-dependency updates into one PR.
- Keep the `github-actions` ecosystem entry.

## 10. pre-commit, editor, devcontainer

- `.pre-commit-config.yaml`: bump all `rev`s; fix `default_stages: [commit]` →
  `[pre-commit]`; keep `ruff` + `ruff-format` + `mypy` (mirrors-mypy) + standard
  hygiene hooks; keep the pre-push pytest hook but invoke via `uv run pytest`.
- `.vscode/settings.json`: remove deprecated `python.linting.enabled`; keep Ruff
  as formatter with `source.fixAll` + `source.organizeImports`.
- `.devcontainer/devcontainer.json`: install **uv** (e.g. `ghcr.io/...` uv feature
  or `astral-sh/uv` install) instead of `pip install poetry`; `postCreateCommand:
  "uv sync"`. Keep the Ruff/Python/TOML VS Code extensions.

## 11. Structure & documentation cleanup

- **Delete** `BEST_PRACTICES_ANALYSIS.md` and `IMPLEMENTATION_SUMMARY.md`
  (build-history meta-docs; noise in a copy-and-go template).
- **Rewrite `CLAUDE.md`** as a lean *conventions* document: what the project is,
  the stack, how to run things (nox / uv), structure, and the quality gates —
  not a setup changelog.
- **Rewrite `README.md`** around the uv + nox workflow (install, common commands,
  testing, release-via-trusted-publishing, how to strip library bits for an app).
- **Refresh `CHANGELOG.md`** with this modernization entry (Keep a Changelog +
  commitizen-compatible).
- `.gitignore`: ensure `.python-version` and `uv.lock` are **tracked** (not
  ignored); drop the Poetry-specific `requirements*.txt` export lines.

### New community-health files (lean set)

- `CONTRIBUTING.md` — short: setup with uv, run nox, commit convention
  (conventional commits / commitizen), PR expectations.
- `SECURITY.md` — how to report vulnerabilities, supported versions.
- `.github/PULL_REQUEST_TEMPLATE.md` — concise checklist.

## 12. Acceptance criteria

1. `uv sync` succeeds on a clean checkout; `uv.lock` present, `poetry.lock` gone.
2. `nox -s lint type_check tests` passes; mypy runs in strict mode clean.
3. Coverage ≥ 80%; tests pass on 3.12 / 3.13 / 3.14.
4. `uv build` produces sdist + wheel; the wheel contains `py.typed`.
5. No version contradictions across `requires-python`, CI matrix, Ruff/mypy targets.
6. `__version__` resolves via `importlib.metadata` and matches `[project].version`.
7. Sample code (dataclass, CLI entry point, parametrize/fixture/mock tests) present and tested; `quickython` console script runs.
8. CI and release workflows are uv-based; release uses Trusted Publishing (no tokens).
9. Meta-docs removed; `CLAUDE.md`/`README.md` rewritten; lean health files added.
10. Repo contains no stale Poetry references (Makefile, snok/install-poetry, `poetry run`, export targets).

## 13. Risks / notes

- **uv.lock churn**: regenerated lock will differ substantially from poetry.lock; expected.
- **Strict mypy** may surface issues in sample code — samples will be written to pass strict.
- **Trusted Publishing** requires a one-time PyPI project/publisher config by the maintainer; documented, not automatable here.
- Migration is non-additive (Poetry artifacts removed); this is intended for a template.
