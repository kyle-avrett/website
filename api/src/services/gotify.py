from urllib.parse import urlparse

from gotify import AsyncGotify

from src.settings import settings


async def create_message(title: str, message: str, token: str, token_name: str) -> None:
    if not settings.GOTIFY_URL:
        raise ValueError("GOTIFY_URL not set")

    if not token:
        raise ValueError(f"{token_name} not set")

    url = urlparse(settings.GOTIFY_URL)
    if url.scheme not in {"http", "https"} or not url.hostname:
        raise ValueError("GOTIFY_URL must be http or https")

    client = AsyncGotify(
        base_url=settings.GOTIFY_URL.rstrip("/"),
        app_token=token,
    )
    await client.create_message(message, title=title)


async def notify_website(title: str, message: str) -> None:
    await create_message(
        title, message, settings.GOTIFY_TOKEN_WEBSITE, "GOTIFY_TOKEN_WEBSITE"
    )


async def notify_social_media(title: str, message: str) -> None:
    await create_message(
        title,
        message,
        settings.GOTIFY_TOKEN_SOCIAL_MEDIA,
        "GOTIFY_TOKEN_SOCIAL_MEDIA",
    )
