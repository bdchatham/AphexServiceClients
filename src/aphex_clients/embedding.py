"""Embedding service client with retry logic.

Wraps the generated OpenAPI client with a RetryingClient for resilience.
"""

from typing import List

from .http import RetryingClient
from .generated.embedding.client import Client as GeneratedClient
from .generated.embedding.api.default import create_embeddings, health_check
from .generated.embedding.models import EmbeddingRequest


class EmbeddingClient:
    """Client for the Aphex embedding service.
    
    Wraps the generated OpenAPI client with automatic retry on transient failures.
    
    Usage:
        async with EmbeddingClient(base_url="http://embedding-svc:8000") as client:
            embeddings = await client.embed(["Hello world"])
    """
    
    def __init__(
        self,
        base_url: str,
        model: str = "BAAI/bge-base-en-v1.5",
        timeout: float = 60.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self._http_client = RetryingClient(base_url=self.base_url, timeout=timeout)
        self._client = GeneratedClient(
            base_url=self.base_url,
            raise_on_unexpected_status=True,
        ).set_async_httpx_client(self._http_client)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self._http_client.aclose()
    
    async def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts.
        
        Args:
            texts: List of strings to embed
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        request = EmbeddingRequest(input_=texts, model=self.model)
        response = await create_embeddings.asyncio(client=self._client, body=request)
        
        return [item.embedding for item in response.data]
    
    async def embed_single(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        embeddings = await self.embed([text])
        return embeddings[0]
    
    async def health_check(self) -> bool:
        """Check if service is healthy."""
        try:
            response = await health_check.asyncio_detailed(client=self._client)
            return response.status_code.value == 200
        except Exception:
            return False
