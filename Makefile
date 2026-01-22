.PHONY: generate-clients check-clients install-dev

install-dev:
	pip install -e ".[dev]"

generate-clients:
	./scripts/generate-clients.sh

check-clients:
	@echo "Checking if generated clients match committed code..."
	@./scripts/generate-clients.sh
	@if git diff --exit-code src/aphex_clients/generated/; then \
		echo "✓ Generated clients are up to date"; \
	else \
		echo "✗ Generated clients are out of sync with OpenAPI specs"; \
		echo "Run 'make generate-clients' and commit the changes"; \
		exit 1; \
	fi
