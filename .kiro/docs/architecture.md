# Architecture

## System Design

AphexServiceClients follows a layered architecture:

1. **Base HTTP Layer** - `RetryingClient` provides resilient HTTP communication
2. **Service Client Layer** - Service-specific clients (e.g., `EmbeddingClient`) provide typed APIs
3. **OpenAPI Specs** - Define API contracts for code generation

## Components

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

High-level client for the Aphex embedding service. Provides methods for generating text embeddings using the OpenAI-compatible API format.

**Methods:**
- `embed(texts: List[str])` - Generate embeddings for multiple texts
- `embed_single(text: str)` - Generate embedding for a single text
- `health_check()` - Check service health

**Default Configuration:**
- Model: `BAAI/bge-base-en-v1.5`
- Timeout: 60 seconds

**Source**
- `src/aphex_clients/embedding.py`

### QueryClient

Client for the Archon Knowledge Base Query Service. Provides semantic search over ingested documents.

**Methods:**
- `retrieve(query: str, k: int = None)` - Search for relevant document chunks
- `health_check()` - Check service health
- `ready_check()` - Check if service and dependencies are ready

**Default Configuration:**
- Timeout: 30 seconds

**Source**
- `src/aphex_clients/query.py`

## Technology Stack

- **Python 3.11+** - Runtime
- **httpx** - Async HTTP client
- **tenacity** - Retry logic with exponential backoff
- **pydantic** - Data validation (for generated clients)

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
