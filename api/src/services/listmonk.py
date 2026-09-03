from dataclasses import dataclass
from typing import Any, Self
from urllib.parse import urlparse

import httpx2

from src.settings import settings


@dataclass(frozen=True)
class ListmonkSubscriber:
    id: int
    email: str
    name: str
    created_at: str | None = None
    updated_at: str | None = None
    uuid: str | None = None
    attribs: dict[str, object] | None = None
    status: str | None = None
    lists: list[int] | None = None

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Self:
        return cls(**data)


async def create_subscriber(
    name: str, email: str, source: str | None = None
) -> ListmonkSubscriber:
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
        return ListmonkSubscriber.from_data(response.json()["data"])


async def send_welcome_email(listmonk_subscriber: ListmonkSubscriber) -> None:
    if not settings.LISTMONK_TEMPLATE_WELCOME_EMAIL:
        raise ValueError("LISTMONK_TEMPLATE_WELCOME_EMAIL not set")

    async with httpx2.AsyncClient(
        auth=httpx2.BasicAuth(settings.LISTMONK_USER, settings.LISTMONK_PASS),
        timeout=10,
    ) as client:
        response = await client.post(
            f"{settings.LISTMONK_URL.rstrip('/')}/api/tx",
            json={
                "subscriber_id": listmonk_subscriber.id,
                "template_id": settings.LISTMONK_TEMPLATE_WELCOME_EMAIL,
            },
        )
        response.raise_for_status()
