# Overview

## Purpose

AphexServiceClients provides generated API clients for Aphex platform services with built-in retry logic, exponential backoff, and jitter. It serves as the shared client library for all services that need to communicate with Aphex platform APIs.

The package eliminates the need for each consuming service to implement its own HTTP client with retry logic, ensuring consistent resilience patterns across the platform.

## Archon Integration

This repository is ingested by the **Archon** RAG system, which reads all Markdown files under `.kiro/docs/` to build mental models for sourcing code and architectural information.

Documentation in this repository follows the Archon documentation contract defined in `CLAUDE.md` at the repo root.

## Key Concepts

### RetryingClient

A base HTTP client built on `httpx.AsyncClient` that automatically retries failed requests with exponential backoff and jitter. All service-specific clients use this as their foundation.

### Service Clients

High-level clients for specific platform services (e.g., `EmbeddingClient`, `QueryClient`). These wrap the `RetryingClient` and provide typed methods for each API endpoint.

### OpenAPI Specifications

Service APIs are defined using OpenAPI 3.1 specifications stored in `openapi/`. These specs serve as the source of truth for API contracts and can be used to generate clients.

## Installation

```bash
pip install aphex-service-clients
```

## Quick Start

```python
from aphex_clients import EmbeddingClient, QueryClient

# Generate embeddings
async with EmbeddingClient(base_url="http://embedding-svc:8000") as client:
    embeddings = await client.embed(["Hello world", "Another text"])

# Query knowledge base
async with QueryClient(base_url="http://query:8080") as client:
    results = await client.retrieve("How do I deploy?")
    for chunk in results:
        print(f"{chunk.source}: {chunk.content}")
```

## Related Repositories

- **ArchonKnowledgeBaseInfrastructure** - Primary consumer; uses `EmbeddingClient` for document embedding
- **ArchonAgent** - May use clients for service communication

**Source**
- `CLAUDE.md`
- `README.md`
- `src/aphex_clients/__init__.py`
