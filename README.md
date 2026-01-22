# Aphex Service Clients

Generated API clients for Aphex platform services with built-in retry logic, exponential backoff, and jitter.

## Installation

```bash
pip install aphex-service-clients
```

## Usage

```python
from aphex_clients.embedding import EmbeddingClient

async with EmbeddingClient(base_url="http://embedding-svc:8000") as client:
    response = await client.create_embeddings(input=["Hello world"])
    embeddings = [d.embedding for d in response.data]
```

## Regenerating Clients

When OpenAPI specs change:

```bash
pip install -e ".[dev]"
./scripts/generate-clients.sh
```

## Services

- **Embedding Service** - OpenAI-compatible embedding generation
