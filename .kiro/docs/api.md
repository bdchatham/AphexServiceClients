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

## OpenAPI Specification: Embedding Service

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
