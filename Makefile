.PHONY: fmt
fmt: 
	ruff check .
	ruff format .

.PHONY: lint
lint:
	ruff check .

.PHONY: install
install:
	mcp install monzo_mcp/server.py:mcp -f .env --name monzo-mcp
