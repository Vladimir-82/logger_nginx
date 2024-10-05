.PHONY: lint test
lint:
	pre-commit run --all-files

test:
	pytest tests

make