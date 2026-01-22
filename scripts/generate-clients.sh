#!/usr/bin/env bash
# Generate Python clients from OpenAPI specs

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR/.."
OPENAPI_DIR="$ROOT_DIR/openapi"
OUTPUT_DIR="$ROOT_DIR/src/aphex_clients/generated"

rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Generate embedding service client
openapi-python-client generate \
  --path "$OPENAPI_DIR/embedding-service.json" \
  --output-path "$OUTPUT_DIR/embedding" \
  --meta none

# Generate query service client
openapi-python-client generate \
  --path "$OPENAPI_DIR/query-service.json" \
  --output-path "$OUTPUT_DIR/query" \
  --meta none

# Create __init__.py to expose clients
cat > "$OUTPUT_DIR/__init__.py" << 'EOF'
"""Generated API clients."""
EOF

echo "Clients generated in $OUTPUT_DIR"
