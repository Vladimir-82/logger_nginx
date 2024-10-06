.PHONY: lint test custom default
lint:
	pre-commit run --all-files

test:
	pytest tests

custom:
	python3 log_analyzer.py --config config.json

default:
	python3 log_analyzer.py
