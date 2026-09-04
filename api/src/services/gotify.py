from urllib.parse import urlparse

from gotify import AsyncGotify

from src.settings import settings


async def send_message(message: str, title: str = "New subscriber") -> None:
    if not settings.GOTIFY_URL:
        raise ValueError("GOTIFY_URL not set")

    if not settings.GOTIFY_TOKEN_WEBSITE:
        raise ValueError("GOTIFY_TOKEN_WEBSITE not set")

    url = urlparse(settings.GOTIFY_URL)
    if url.scheme not in {"http", "https"} or not url.hostname:
        raise ValueError("GOTIFY_URL must be http or https")

    client = AsyncGotify(
        base_url=settings.GOTIFY_URL.rstrip("/"),
        app_token=settings.GOTIFY_TOKEN_WEBSITE,
    )
    await client.create_message(message, title=title)
