import httpx
from app.core.exceptions import (
    ServiceCommunicationError,
    ServiceTimeoutError,
)



class HTTPClient:
    def __init__(self) -> None:
        self.client: httpx.AsyncClient | None = None

    async def start(self) -> None:
        if self.client is not None:
            return

        timeout = httpx.Timeout(
            timeout=10.0,
            connect=5.0,
        )

        limits = httpx.Limits(
            max_connections=100,
            max_keepalive_connections=20,
        )

        self.client = httpx.AsyncClient(
            timeout=timeout,
            limits=limits,
            follow_redirects=False,
        )

    async def close(self) -> None:
        if self.client is None:
            return

        client = self.client
        self.client = None

        await client.aclose()

    def get_client(self) -> httpx.AsyncClient:
        if self.client is None:
            raise RuntimeError(
                "HTTP client has not been initialized"
            )

        return self.client

    async def request(
        self,
        method: str,
        url: str,
        **kwargs,
    ) -> httpx.Response:
        client = self.get_client()

        try:
            return await client.request(
                method=method,
                url=url,
                **kwargs,
            )

        except httpx.TimeoutException as exc:
            raise ServiceTimeoutError(
                "Downstream service request timed out"
            ) from exc

        except httpx.RequestError as exc:
            raise ServiceCommunicationError(
                "Unable to communicate with downstream service"
            ) from exc


http_client = HTTPClient()
