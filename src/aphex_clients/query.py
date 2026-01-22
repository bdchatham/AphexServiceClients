"""Query service client with retry logic.

Client for the Archon Knowledge Base Query Service.
"""

from dataclasses import dataclass
from typing import List, Optional

from .http import RetryingClient


@dataclass
class ChunkResult:
    """A retrieved document chunk."""
    content: str
    source: str
    chunk_index: int
    score: float


class QueryClient:
    """Client for the Archon Knowledge Base Query Service.
    
    Provides semantic search over ingested documents with automatic retry.
    
    Usage:
        async with QueryClient(base_url="http://query:8080") as client:
            results = await client.retrieve("How do I deploy?")
            for chunk in results:
                print(f"{chunk.source}: {chunk.content}")
    """
    
    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self._client = RetryingClient(base_url=self.base_url, timeout=timeout)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self._client.aclose()
    
    async def retrieve(
        self,
        query: str,
        k: Optional[int] = None,
    ) -> List[ChunkResult]:
        """Retrieve relevant document chunks for a query.
        
        Args:
            query: Search query text
            k: Number of results to return (optional)
            
        Returns:
            List of ChunkResult ordered by relevance
        """
        payload = {"query": query}
        if k is not None:
            payload["k"] = k
        
        response = await self._client.post("/v1/retrieve", json=payload)
        response.raise_for_status()
        data = response.json()
        
        return [
            ChunkResult(
                content=chunk["content"],
                source=chunk["source"],
                chunk_index=chunk["chunk_index"],
                score=chunk["score"],
            )
            for chunk in data["chunks"]
        ]
    
    async def health_check(self) -> bool:
        """Check if service is healthy."""
        try:
            response = await self._client.get("/health")
            return response.status_code == 200
        except Exception:
            return False
    
    async def ready_check(self) -> bool:
        """Check if service is ready (all dependencies healthy)."""
        try:
            response = await self._client.get("/ready")
            return response.status_code == 200
        except Exception:
            return False
