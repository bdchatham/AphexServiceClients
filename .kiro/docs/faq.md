# FAQ

## General Questions

### What is this repository for?

AphexServiceClients provides shared API clients for Aphex platform services. It ensures consistent retry logic, exponential backoff, and jitter across all services that communicate with platform APIs.

### How does this fit into the larger system?

This package is a dependency for services that need to call Aphex platform APIs. For example, `ArchonKnowledgeBaseInfrastructure` uses `EmbeddingClient` to generate embeddings for documents.

### Why not just use httpx directly?

Using `httpx` directly requires each service to implement its own retry logic. This package provides:
- Consistent retry behavior across all services
- Exponential backoff with jitter to prevent thundering herd
- Typed clients for better developer experience

## Development Questions

### How do I add a new service client?

1. Add the OpenAPI spec to `openapi/` directory
2. Create a client class in `src/aphex_clients/` that uses `RetryingClient`
3. Export the client from `src/aphex_clients/__init__.py`
4. Update documentation in `.kiro/docs/`

### How do I run tests?

```bash
pip install -e ".[dev]"
pytest
```

### How do I regenerate clients from OpenAPI specs?

```bash
./scripts/generate-clients.sh
```

This runs automatically via GitHub Actions when specs change.

## Operational Questions

### What happens when a service is unavailable?

The client automatically retries up to 5 times with exponential backoff:
- 1st retry: ~1 second wait
- 2nd retry: ~2 seconds wait
- 3rd retry: ~4 seconds wait
- 4th retry: ~8 seconds wait
- 5th retry: ~16 seconds wait (capped at 60s)

Random jitter (0-5 seconds) is added to each wait to prevent synchronized retries.

### How do I increase the timeout for slow services?

Pass a custom timeout to the client constructor:

```python
client = EmbeddingClient(base_url="...", timeout=120.0)
```

### What exceptions should I catch?

After all retries are exhausted:
- `httpx.ConnectError` - Service unreachable
- `httpx.TimeoutException` - Request timed out
- `httpx.HTTPStatusError` - Service returned error status (not retried)

### What service URLs should I use in Kubernetes?

Use cluster-internal service names:

```python
# Same namespace
EmbeddingClient(base_url="http://embedding-svc:8000")

# Cross-namespace (fully qualified)
QueryClient(base_url="http://query.archon-knowledge-base.svc.cluster.local:8080")
```

See `operations.md` for complete Kubernetes deployment guidance.

### How do I configure the embedding model?

Pass the model name to the `EmbeddingClient` constructor:

```python
client = EmbeddingClient(
    base_url="http://embedding-svc:8000",
    model="BAAI/bge-base-en-v1.5"  # Default
)
```

The model must be supported by the embedding service deployment.

## Archon-Specific Questions

### How is this repository ingested by Archon?

Archon reads all Markdown files under `.kiro/docs/` from this public GitHub repository. Documentation follows the contract defined in `CLAUDE.md`.

### How do I update documentation?

Update the relevant files under `.kiro/docs/` and ensure changes are grounded in code. Include "Source" references to relevant files. Do not create new documentation files; add content to the existing 6 files.

**Source**
- `CLAUDE.md`
- `.kiro/steering/archon-docs.md`
- `src/aphex_clients/http.py`
