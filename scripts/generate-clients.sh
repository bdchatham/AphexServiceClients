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

# Create __init__.py to expose clients
cat > "$OUTPUT_DIR/__init__.py" << 'EOF'
"""Generated API clients."""
from .embedding.client import Client as EmbeddingClientBase
from .embedding.api.default import create_embeddings, health_check
from .embedding import models as embedding_models

__all__ = [
    "EmbeddingClientBase",
    "create_embeddings", 
    "health_check",
    "embedding_models",
]
EOF

echo "Clients generated in $OUTPUT_DIR"
