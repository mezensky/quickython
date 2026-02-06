.PHONY: install
install:
	poetry install
	poetry run pre-commit install

.PHONY: lint
lint:
	poetry run ruff check src/quickython/ tests/
	poetry run ruff format --check src/quickython/ tests/
	poetry run mypy src/quickython/ tests/

.PHONY: format
format:
	poetry run ruff check --fix src/quickython/ tests/
	poetry run ruff format src/quickython/ tests/

.PHONY: test
test:
	poetry run pytest -n auto --cov-fail-under=80

.PHONY: test-cov
test-cov:
	poetry run pytest --cov=quickython --cov-report=html --cov-report=term

.PHONY: test-no-parallel
test-no-parallel:
	poetry run pytest --cov-fail-under=80

.PHONY: pre-commit
pre-commit:
	poetry run pre-commit run --all-files

.PHONY: security
security:
	poetry run pip-audit

.PHONY: bump-patch
bump-patch:
	poetry run cz bump --increment PATCH

.PHONY: bump-minor
bump-minor:
	poetry run cz bump --increment MINOR

.PHONY: bump-major
bump-major:
	poetry run cz bump --increment MAJOR

.PHONY: changelog
changelog:
	poetry run cz changelog

.PHONY: docs-check
docs-check:
	poetry run interrogate -v src/quickython/

.PHONY: dead-code
dead-code:
	poetry run vulture src/quickython/ --min-confidence 80

.PHONY: build
build:
	poetry build

.PHONY: publish-test
publish-test: build
	poetry publish --repository testpypi

.PHONY: publish
publish: build
	poetry publish

.PHONY: export-requirements
export-requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
	poetry export -f requirements.txt --output requirements-dev.txt --with dev --without-hashes

.PHONY: clean
clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
