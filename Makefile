.PHONY: fmt
fmt: 
	ruff check .
	ruff format .

.PHONY: lint
lint:
	ruff check .

