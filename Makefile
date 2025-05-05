.PHONY: fmt
fmt: 
	ruff check .
	ruff format .

.PHONY: lint
lint:
	ruff check .

.PHONY: install_claude
install_claude:
	fastmcp install monzo_mcp/server.py -f .env --name monzo-mcp
