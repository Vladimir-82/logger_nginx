.PHONY: lint test logging
lint:
	pre-commit run --all-files

test:
	pytest tests
