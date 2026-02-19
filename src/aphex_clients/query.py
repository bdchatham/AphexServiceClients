"""Query service client with retry logic.

Wraps the generated OpenAPI client with a RetryingClient for resilience.
"""

from typing import List, Optional

from .http import RetryingClient
from .generated.query.client import Client as GeneratedClient
from .generated.query.api.default import retrieve, health_check, readiness_check
from .generated.query.models import RetrieveRequest, ChunkResult as GeneratedChunkResult


# Re-export the generated ChunkResult for convenience
ChunkResult = GeneratedChunkResult


class QueryClient:
    """Client for the Archon Knowledge Base Query Service.
    
    Wraps the generated OpenAPI client with automatic retry on transient failures.
    
    Usage:
        async with QueryClient(base_url="http://query:8080") as client:
            results = await client.retrieve("How do I deploy?")
            for chunk in results:
                print(f"{chunk.source}: {chunk.content}")
    """
    
    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self._http_client = RetryingClient(base_url=self.base_url, timeout=timeout)
        self._client = GeneratedClient(
            base_url=self.base_url,
            raise_on_unexpected_status=True,
        ).set_async_httpx_client(self._http_client)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self._http_client.aclose()
    
    async def retrieve(
        self,
        query: str,
        k: Optional[int] = None,
    ) -> List[GeneratedChunkResult]:
        """Retrieve relevant document chunks for a query.
        
        Args:
            query: Search query text
            k: Number of results to return (optional)
            
        Returns:
            List of ChunkResult ordered by relevance
        """
        request = RetrieveRequest(query=query, k=k)
        response = await retrieve.asyncio(client=self._client, body=request)
        return response.chunks
    
    async def get_document(self, doc_id: str) -> str:
        """Retrieve full document content by doc_id.
        
        Args:
            doc_id: Document identifier (source path)
            
        Returns:
            Full document content
        """
        import httpx
        response = await self._http_client.post(
            f"{self.base_url}/v1/document",
            json={"doc_id": doc_id},
        )
        response.raise_for_status()
        result = response.json()
        return result["content"]
    
    async def health_check(self) -> bool:
        """Check if service is healthy."""
        try:
            response = await health_check.asyncio_detailed(client=self._client)
            return response.status_code.value == 200
        except Exception:
            return False
    
    async def ready_check(self) -> bool:
        """Check if service is ready (all dependencies healthy)."""
        try:
            response = await readiness_check.asyncio_detailed(client=self._client)
            return response.status_code.value == 200
        except Exception:
            return False
