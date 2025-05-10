.PHONY: fmt
fmt: 
	ruff check .
	ruff format .

.PHONY: lint
lint:
	ruff check .

.PHONY: install
install:
	mcp install /Users/benjaminking/Developer/monzo_mcp/monzo_mcp/__main__.py -f .env --name monzo-mcp --with-editable .
