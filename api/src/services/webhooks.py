import hashlib
import hmac
import json
import time
from typing import Annotated, Literal
from urllib.parse import urlparse

import httpx2
from fastapi import FastAPI, Header
from pydantic import BaseModel

from src.settings import settings

WebhookEventHeader = Annotated[
    str,
    Header(
        alias="x-webhook-event",
        description="Event name. Same value as body.event.",
    ),
]
WebhookTimestampHeader = Annotated[
    str,
    Header(
        alias="x-webhook-timestamp",
        description="Unix timestamp used in signature.",
    ),
]
WebhookSignatureHeader = Annotated[
    str,
    Header(
        alias="x-webhook-signature",
        description="HMAC SHA-256 signature: sha256=<hex> of `{timestamp}.{raw_body}`.",
    ),
]


def register(app: FastAPI) -> None:
    from src.routes.emails import EmailResponse
    from src.routes.social_media import SocialMediaRequest

    class EmailSubscribedWebhook(BaseModel):
        event: Literal["email.subscribed"]
        data: EmailResponse

    class SocialMediaPublishedWebhook(BaseModel):
        event: Literal["social_media.published"]
        data: SocialMediaRequest

    @app.webhooks.post("email.subscribed", summary="Email subscribed")
    def email_subscribed_webhook(
        body: EmailSubscribedWebhook,
        x_webhook_event: WebhookEventHeader,
        x_webhook_timestamp: WebhookTimestampHeader,
        x_webhook_signature: WebhookSignatureHeader,
    ) -> None:
        """
        Sent to every configured WEBHOOK_URLS endpoint after a new email subscriber is stored.
        """

    @app.webhooks.post("social_media.published", summary="Social media published")
    def social_media_published_webhook(
        body: SocialMediaPublishedWebhook,
        x_webhook_event: WebhookEventHeader,
        x_webhook_timestamp: WebhookTimestampHeader,
        x_webhook_signature: WebhookSignatureHeader,
    ) -> None:
        """
        Sent to every configured WEBHOOK_URLS endpoint after a social media post notification.
        """


async def deliver(event: str, data: dict) -> None:
    urls = settings.WEBHOOK_URL_LIST
    if not urls:
        return

    if not settings.WEBHOOK_SECRET:
        raise ValueError("WEBHOOK_SECRET not set")

    body = json.dumps(
        {"event": event, "data": data},
        separators=(",", ":"),
        sort_keys=True,
    ).encode()
    timestamp = str(int(time.time()))
    signature = hmac.new(
        settings.WEBHOOK_SECRET.encode(),
        timestamp.encode() + b"." + body,
        hashlib.sha256,
    ).hexdigest()
    headers = {
        "content-type": "application/json",
        "x-webhook-event": event,
        "x-webhook-timestamp": timestamp,
        "x-webhook-signature": f"sha256={signature}",
    }

    for url in urls:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("WEBHOOK_URLS must contain only http or https URLs")

    async with httpx2.AsyncClient(timeout=10) as client:
        for url in urls:
            response = await client.post(url, content=body, headers=headers)
            response.raise_for_status()
