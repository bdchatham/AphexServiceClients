# Architecture

## System Design

AphexServiceClients follows a layered architecture:

1. **Generated Clients** - Auto-generated from OpenAPI specs, provide typed models and API methods
2. **Wrapper Clients** - Inject `RetryingClient` into generated clients for resilience
3. **Base HTTP Layer** - `RetryingClient` provides retry with exponential backoff and jitter

```
┌─────────────────────────────────────┐
│  EmbeddingClient / QueryClient      │  ← Wrapper layer (retry injection)
├─────────────────────────────────────┤
│  Generated Clients (from OpenAPI)   │  ← Typed models & API methods
├─────────────────────────────────────┤
│  RetryingClient (httpx + tenacity)  │  ← Resilient HTTP transport
└─────────────────────────────────────┘
```

## Components

### Package Exports

The package exports four public classes from `src/aphex_clients/__init__.py`:

- **`EmbeddingClient`** - Client for embedding service
- **`QueryClient`** - Client for Knowledge Base query service
- **`ChunkResult`** - Data class for query results (re-exported from generated code)
- **`RetryingClient`** - Base HTTP client with retry logic (typically not used directly)

**Source**
- `src/aphex_clients/__init__.py`

### Generated Clients

Auto-generated from OpenAPI specs using `openapi-python-client`. Located in `src/aphex_clients/generated/`.

**Generated for each service:**
- `client.py` - Base client with httpx integration
- `models/` - Pydantic-style request/response models
- `api/default/` - Typed async methods for each endpoint

**Generation:**
```bash
make generate-clients
```

**CI Verification:**
The `check-clients` workflow fails if generated code doesn't match committed code, ensuring specs and clients stay in sync.

**Source**
- `src/aphex_clients/generated/`
- `scripts/generate-clients.sh`
- `Makefile`

### RetryingClient

Base async HTTP client that wraps `httpx.AsyncClient` with automatic retry on transient failures.

**Retry Configuration:**
- Max attempts: 5
- Initial wait: 1 second
- Max wait: 60 seconds
- Jitter: up to 5 seconds random delay
- Retried exceptions: `httpx.ConnectError`, `httpx.TimeoutException`

**Source**
- `src/aphex_clients/http.py`

### EmbeddingClient

Wrapper client for the embedding service. Injects `RetryingClient` into the generated client for automatic retry on transient failures.

**Methods:**
- `embed(texts: List[str])` - Generate embeddings for multiple texts
- `embed_single(text: str)` - Generate embedding for a single text
- `health_check()` - Check service health

**Default Configuration:**
- Model: `BAAI/bge-base-en-v1.5`
- Timeout: 60 seconds

**Typical Usage in Kubernetes:**
```python
# Same namespace
EmbeddingClient(base_url="http://embedding-svc:8000")

# Cross-namespace
EmbeddingClient(base_url="http://embedding-svc.archon-knowledge-base:8000")
```

**Source**
- `src/aphex_clients/embedding.py`
- `src/aphex_clients/generated/embedding/`

### QueryClient

Wrapper client for the Archon Knowledge Base Query Service. Injects `RetryingClient` into the generated client for automatic retry.

**Methods:**
- `retrieve(query: str, k: int = None)` - Search for relevant document chunks
- `health_check()` - Check service health
- `ready_check()` - Check if service and dependencies are ready

**Default Configuration:**
- Timeout: 30 seconds

**Typical Usage in Kubernetes:**
```python
# Same namespace
QueryClient(base_url="http://query:8080")

# Cross-namespace
QueryClient(base_url="http://query.archon-knowledge-base.svc.cluster.local:8080")
```

**Source**
- `src/aphex_clients/query.py`
- `src/aphex_clients/generated/query/`

## Technology Stack

- **Python 3.11+** - Runtime
- **httpx** - Async HTTP client
- **tenacity** - Retry logic with exponential backoff
- **attrs** - Data classes for generated models
- **openapi-python-client** - Code generation from OpenAPI specs (dev dependency)

## Architectural Patterns

### Retry with Exponential Backoff and Jitter

All HTTP requests use exponential backoff with jitter to prevent thundering herd problems when services recover from failures.

The `with_retry` decorator from `tenacity` is configured to:
1. Start with 1 second wait
2. Double wait time on each retry (exponential)
3. Add random jitter (0-5 seconds) to spread out retries
4. Cap maximum wait at 60 seconds
5. Stop after 5 attempts

### Context Manager Pattern

Service clients implement async context managers for proper resource cleanup:

```python
async with EmbeddingClient(base_url="...") as client:
    # client is ready to use
    result = await client.embed(["text"])
# client is automatically closed
```

## Dependencies

### Upstream Dependencies

- **Embedding Service** - OpenAI-compatible embedding API (defined in `openapi/embedding-service.json`)
- **Query Service** - Knowledge base retrieval API (defined in `openapi/query-service.json`)

### Downstream Dependencies

- **ArchonKnowledgeBaseInfrastructure** - Uses `EmbeddingClient` for document embedding in the monitor service

**Source**
- `src/aphex_clients/http.py`
- `src/aphex_clients/embedding.py`
- `pyproject.toml`
