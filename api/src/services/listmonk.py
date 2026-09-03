import asyncio
import base64
import json
from http.client import HTTPConnection, HTTPSConnection
from urllib.parse import urlparse

from src.settings import settings


def _create_subscriber(name: str, email: str) -> None:
    # validation
    if not settings.LISTMONK_URL:
        raise ValueError("LISTMONK_URL not set")

    if not settings.LISTMONK_LIST:
        raise ValueError("LISTMONK_LIST not set")

    url = urlparse(settings.LISTMONK_URL)
    if url.scheme not in {"http", "https"} or not url.hostname:
        raise ValueError("LISTMONK_URL must be http or https")

    # payload setup
    path = f"{url.path.rstrip('/')}/api/subscribers"
    body = json.dumps(
        {
            "name": name,
            "email": email,
            "status": "enabled",
            "lists": [settings.LISTMONK_LIST],
        }
    )
    token = base64.b64encode(
        f"{settings.LISTMONK_USER}:{settings.LISTMONK_PASS}".encode()
    ).decode()

    # execute
    connection_type = HTTPSConnection if url.scheme == "https" else HTTPConnection
    connection = connection_type(url.hostname, url.port, timeout=10)
    try:
        connection.request(
            "POST",
            path,
            body=body,
            headers={
                "Authorization": f"Basic {token}",
                "Content-Type": "application/json",
            },
        )
        response = connection.getresponse()
        response.read()
        if response.status >= 400:
            raise RuntimeError(f"listmonk returned {response.status}")
    finally:
        connection.close()


async def create_subscriber(name: str, email: str) -> None:
    await asyncio.to_thread(_create_subscriber, name, email)
