# Data Models

## OpenAPI Schema: EmbeddingRequest

Request body for the `/v1/embeddings` endpoint.

```json
{
  "type": "object",
  "required": ["input"],
  "properties": {
    "input": {
      "oneOf": [
        {"type": "string"},
        {"type": "array", "items": {"type": "string"}}
      ]
    },
    "model": {
      "type": "string",
      "default": "BAAI/bge-base-en-v1.5"
    }
  }
}
```

**Fields:**
- `input` - Single string or array of strings to embed (required)
- `model` - Model name to use for embedding (optional, defaults to `BAAI/bge-base-en-v1.5`)

**Source**
- `openapi/embedding-service.json`

## OpenAPI Schema: EmbeddingResponse

Response body from the `/v1/embeddings` endpoint.

```json
{
  "type": "object",
  "properties": {
    "object": {"type": "string", "default": "list"},
    "data": {
      "type": "array",
      "items": {"$ref": "#/components/schemas/EmbeddingData"}
    },
    "model": {"type": "string"},
    "usage": {"$ref": "#/components/schemas/EmbeddingUsage"}
  }
}
```

**Fields:**
- `object` - Always `"list"`
- `data` - Array of `EmbeddingData` objects
- `model` - Model name used for embedding
- `usage` - Token usage information

**Source**
- `openapi/embedding-service.json`

## OpenAPI Schema: EmbeddingData

Individual embedding result within the response.

```json
{
  "type": "object",
  "properties": {
    "object": {"type": "string", "default": "embedding"},
    "embedding": {"type": "array", "items": {"type": "number"}},
    "index": {"type": "integer"}
  }
}
```

**Fields:**
- `object` - Always `"embedding"`
- `embedding` - Vector of floats (768 dimensions for `BAAI/bge-base-en-v1.5`)
- `index` - Position in the input array

**Source**
- `openapi/embedding-service.json`

## OpenAPI Schema: EmbeddingUsage

Token usage information in the response.

```json
{
  "type": "object",
  "properties": {
    "prompt_tokens": {"type": "integer"},
    "total_tokens": {"type": "integer"}
  }
}
```

**Fields:**
- `prompt_tokens` - Approximate tokens in the input
- `total_tokens` - Total tokens processed

**Source**
- `openapi/embedding-service.json`

## Embedding Vector Dimensions

The `BAAI/bge-base-en-v1.5` model produces 768-dimensional vectors. Each embedding is a list of 768 floating-point numbers.

When storing embeddings in vector databases (e.g., Qdrant), ensure the collection is configured with `size: 768`.

**Source**
- `openapi/embedding-service.json`

## OpenAPI Schema: RetrieveRequest

Request body for the `/v1/retrieve` endpoint.

```json
{
  "type": "object",
  "required": ["query"],
  "properties": {
    "query": {"type": "string", "description": "Search query text"},
    "k": {"type": "integer", "description": "Number of results to return"}
  }
}
```

**Fields:**
- `query` - Search query text (required)
- `k` - Number of results to return (optional, uses server default)

**Source**
- `openapi/query-service.json`

## OpenAPI Schema: RetrieveResponse

Response body from the `/v1/retrieve` endpoint.

```json
{
  "type": "object",
  "properties": {
    "chunks": {"type": "array", "items": {"$ref": "#/components/schemas/ChunkResult"}},
    "query": {"type": "string"}
  }
}
```

**Fields:**
- `chunks` - Array of `ChunkResult` objects
- `query` - Original query string

**Source**
- `openapi/query-service.json`

## OpenAPI Schema: ChunkResult

Individual chunk result within the response.

```json
{
  "type": "object",
  "properties": {
    "content": {"type": "string", "description": "Chunk text content"},
    "source": {"type": "string", "description": "Source document path"},
    "chunk_index": {"type": "integer", "description": "Index within source document"},
    "score": {"type": "number", "description": "Similarity score"}
  }
}
```

**Fields:**
- `content` - The text content of the chunk
- `source` - Full path to source document (e.g., GitHub URL)
- `chunk_index` - Position of this chunk within the source document
- `score` - Cosine similarity score (0-1, higher is more relevant)

**Source**
- `openapi/query-service.json`
