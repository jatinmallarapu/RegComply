# Run the regcomply example with the same inputs documented in the quickstart.
.PHONY: dev test lint

dev:
	python regcomply.py ask "What does FINRA say about misleading advertising?"

test:
	python -m pytest --cov=regcomply --cov-fail-under=70

lint:
	ruff check .
	ruff format --check .
	mypy regcomply.py
