from urllib.parse import urlparse

import httpx2

from src.settings import settings


async def create_subscriber(name: str, email: str, source: str | None = None) -> None:
    # validation
    if not settings.LISTMONK_URL:
        raise ValueError("LISTMONK_URL not set")

    if not settings.LISTMONK_LIST:
        raise ValueError("LISTMONK_LIST not set")

    url = urlparse(settings.LISTMONK_URL)
    if url.scheme not in {"http", "https"} or not url.hostname:
        raise ValueError("LISTMONK_URL must be http or https")

    # execute
    async with httpx2.AsyncClient(
        auth=httpx2.BasicAuth(settings.LISTMONK_USER, settings.LISTMONK_PASS),
        timeout=10,
    ) as client:
        response = await client.post(
            f"{settings.LISTMONK_URL.rstrip('/')}/api/subscribers",
            json={
                "name": name,
                "email": email,
                "status": "enabled",
                "lists": [settings.LISTMONK_LIST],
                "attribs": {"source": source} if source else {},
            },
        )
        response.raise_for_status()
