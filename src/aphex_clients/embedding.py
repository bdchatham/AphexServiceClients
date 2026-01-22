"""Embedding service client with retry logic.

Wraps the generated OpenAPI client with exponential backoff and jitter.
"""

from typing import List

from ..http import RetryingClient


class EmbeddingClient:
    """Client for the Aphex embedding service.
    
    Provides embedding generation with automatic retry on transient failures.
    
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
        self._client = RetryingClient(base_url=self.base_url, timeout=timeout)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self._client.aclose()
    
    async def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts.
        
        Args:
            texts: List of strings to embed
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        response = await self._client.post(
            "/v1/embeddings",
            json={"input": texts, "model": self.model},
        )
        response.raise_for_status()
        data = response.json()
        return [item["embedding"] for item in data["data"]]
    
    async def embed_single(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        embeddings = await self.embed([text])
        return embeddings[0]
    
    async def health_check(self) -> bool:
        """Check if service is healthy."""
        try:
            response = await self._client.get("/health")
            return response.status_code == 200
        except Exception:
            return False
