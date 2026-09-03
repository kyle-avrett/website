from urllib.parse import urlparse

from gotify import AsyncGotify

from src.settings import settings


async def send_message(message: str, title: str = "New subscriber") -> None:
    if not settings.GOTIFY_URL:
        raise ValueError("GOTIFY_URL not set")

    if not settings.GOTIFY_PASS:
        raise ValueError("GOTIFY_PASS not set")

    url = urlparse(settings.GOTIFY_URL)
    if url.scheme not in {"http", "https"} or not url.hostname:
        raise ValueError("GOTIFY_URL must be http or https")

    async with AsyncGotify(
        base_url=settings.GOTIFY_URL.rstrip("/"),
        app_token=settings.GOTIFY_PASS,
    ) as client:
        await client.create_message(message, title=title)
