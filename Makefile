MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

PYTHON_CODE = examples/ tauon/ tests/
PYTEST_FLAGS = --quiet --cov=tauon --cov-fail-under=100 --cov-report=term-missing tests/


.PHONY: all
all: install test check


.PHONY: check
check: check-code-format check-code-quality check-dependencies


.PHONY: check-code-format
check-code-format:
	poetry run black --check --quiet $(PYTHON_CODE)
	poetry run isort --check-only $(PYTHON_CODE)


.PHONY: check-code-quality
check-code-quality:
	poetry run bandit --recursive --skip B101 --quiet $(PYTHON_CODE)
	poetry run pylint $(PYTHON_CODE)


.PHONY: check-dependencies
check-dependencies:
	poetry run safety check --bare
	trivy fs .


.PHONY: install
install:
	poetry install


.PHONY: test
test:
	poetry run py.test $(PYTEST_FLAGS)
