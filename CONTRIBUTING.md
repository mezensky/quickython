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
