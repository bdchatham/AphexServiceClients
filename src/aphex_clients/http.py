"""HTTP client with retry, exponential backoff, and jitter.

Provides a base httpx client that generated OpenAPI clients can use.
"""

import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential_jitter,
    retry_if_exception_type,
)


def with_retry(
    max_attempts: int = 5,
    initial: float = 1.0,
    max_wait: float = 60.0,
    jitter: float = 5.0,
):
    """Retry decorator with exponential backoff and jitter."""
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential_jitter(initial=initial, max=max_wait, jitter=jitter),
        retry=retry_if_exception_type((httpx.ConnectError, httpx.TimeoutException)),
        reraise=True,
    )


class RetryingClient(httpx.AsyncClient):
    """Async HTTP client with automatic retry on transient failures.
    
    Wraps httpx.AsyncClient with exponential backoff and jitter for
    ConnectError and TimeoutException.
    
    Usage:
        async with RetryingClient(base_url="http://service:8000") as client:
            response = await client.post("/endpoint", json=data)
    """
    
    @with_retry()
    async def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Make request with retry logic."""
        return await super().request(method, url, **kwargs)
