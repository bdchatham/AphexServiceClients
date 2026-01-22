# API

## EmbeddingClient

Client for the Aphex embedding service with automatic retry logic.

### Constructor

```python
EmbeddingClient(
    base_url: str,
    model: str = "BAAI/bge-base-en-v1.5",
    timeout: float = 60.0
)
```

**Parameters:**
- `base_url` - Base URL of the embedding service (e.g., `http://embedding-svc:8000`)
- `model` - Embedding model name (default: `BAAI/bge-base-en-v1.5`)
- `timeout` - Request timeout in seconds (default: 60.0)

### Methods

#### embed(texts: List[str]) -> List[List[float]]

Generate embeddings for multiple texts.

```python
async with EmbeddingClient(base_url="http://embedding-svc:8000") as client:
    embeddings = await client.embed(["Hello world", "Another text"])
    # embeddings[0] is the vector for "Hello world"
    # embeddings[1] is the vector for "Another text"
```

**Parameters:**
- `texts` - List of strings to embed

**Returns:**
- List of embedding vectors (each vector is a list of floats)

**Raises:**
- `httpx.HTTPStatusError` - If the service returns an error status

#### embed_single(text: str) -> List[float]

Generate embedding for a single text. Convenience wrapper around `embed()`.

```python
async with EmbeddingClient(base_url="http://embedding-svc:8000") as client:
    vector = await client.embed_single("Hello world")
```

**Parameters:**
- `text` - Single string to embed

**Returns:**
- Embedding vector as a list of floats

#### health_check() -> bool

Check if the embedding service is healthy.

```python
async with EmbeddingClient(base_url="http://embedding-svc:8000") as client:
    is_healthy = await client.health_check()
```

**Returns:**
- `True` if service responds with 200 OK, `False` otherwise

**Source**
- `src/aphex_clients/embedding.py`

## RetryingClient

Base HTTP client with automatic retry. Typically not used directly; service clients use it internally.

### Constructor

```python
RetryingClient(
    base_url: str = None,
    timeout: float = None,
    **kwargs
)
```

Accepts all parameters supported by `httpx.AsyncClient`.

### Retry Behavior

All requests automatically retry on:
- `httpx.ConnectError` - Connection failures
- `httpx.TimeoutException` - Request timeouts

Retry configuration:
- Max attempts: 5
- Initial wait: 1 second
- Max wait: 60 seconds
- Jitter: 0-5 seconds

**Source**
- `src/aphex_clients/http.py`

## QueryClient

Client for the Archon Knowledge Base Query Service with automatic retry logic.

### Constructor

```python
QueryClient(
    base_url: str,
    timeout: float = 30.0
)
```

**Parameters:**
- `base_url` - Base URL of the query service (e.g., `http://query:8080`)
- `timeout` - Request timeout in seconds (default: 30.0)

### Methods

#### retrieve(query: str, k: int = None) -> List[ChunkResult]

Search for relevant document chunks.

```python
async with QueryClient(base_url="http://query:8080") as client:
    results = await client.retrieve("How do I deploy?", k=5)
    for chunk in results:
        print(f"[{chunk.score:.2f}] {chunk.source}")
        print(chunk.content)
```

**Parameters:**
- `query` - Search query text
- `k` - Number of results to return (optional, uses server default)

**Returns:**
- List of `ChunkResult` objects ordered by relevance

#### health_check() -> bool

Check if service is healthy.

#### ready_check() -> bool

Check if service and all dependencies (embedding service, vector store) are ready.

### ChunkResult

```python
@dataclass
class ChunkResult:
    content: str      # Chunk text content
    source: str       # Source document path
    chunk_index: int  # Index within source document
    score: float      # Similarity score (0-1)
```

**Source**
- `src/aphex_clients/query.py`

## OpenAPI Specification: Query Service

The embedding service implements an OpenAI-compatible API.

### POST /v1/embeddings

Generate embeddings for input text(s).

**Request:**
```json
{
  "input": ["text1", "text2"],
  "model": "BAAI/bge-base-en-v1.5"
}
```

**Response:**
```json
{
  "object": "list",
  "data": [
    {"object": "embedding", "embedding": [0.1, 0.2, ...], "index": 0},
    {"object": "embedding", "embedding": [0.3, 0.4, ...], "index": 1}
  ],
  "model": "BAAI/bge-base-en-v1.5",
  "usage": {"prompt_tokens": 10, "total_tokens": 10}
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{"status": "healthy"}
```

**Source**
- `openapi/embedding-service.json`

## OpenAPI Specification: Query Service

The query service provides semantic search over ingested documents.

### POST /v1/retrieve

Retrieve relevant document chunks for a query.

**Request:**
```json
{
  "query": "How do I deploy the application?",
  "k": 5
}
```

**Response:**
```json
{
  "chunks": [
    {
      "content": "To deploy the application, run `npm run deploy`...",
      "source": "https://github.com/org/repo/.kiro/docs/operations.md",
      "chunk_index": 3,
      "score": 0.89
    }
  ],
  "query": "How do I deploy the application?"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{"status": "healthy"}
```

### GET /ready

Readiness check - verifies embedding service and vector store connectivity.

**Response:**
```json
{
  "status": "ready",
  "embedding_service": "healthy",
  "vector_store": "healthy"
}
```

**Source**
- `openapi/query-service.json`
