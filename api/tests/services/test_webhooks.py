import hashlib
import hmac
import json

import anyio
import pytest

from src.services import webhooks


def run_deliver(event="thing.happened", data=None):
    return anyio.run(webhooks.deliver, event, data or {"id": 7})


def test_deliver_noops_without_urls(monkeypatch):
    class FakeClient:
        def __init__(self, **kwargs):
            raise AssertionError("client should not be created")

    monkeypatch.setattr(webhooks.settings, "WEBHOOK_URLS", "")
    monkeypatch.setattr(webhooks.httpx2, "AsyncClient", FakeClient)

    run_deliver()


def test_deliver_requires_secret(monkeypatch):
    monkeypatch.setattr(webhooks.settings, "WEBHOOK_URLS", "https://example.com/hook")
    monkeypatch.setattr(webhooks.settings, "WEBHOOK_SECRET", "")

    with pytest.raises(ValueError, match="WEBHOOK_SECRET not set"):
        run_deliver()


def test_deliver_rejects_invalid_url(monkeypatch):
    monkeypatch.setattr(webhooks.settings, "WEBHOOK_URLS", "ftp://example.com/hook")
    monkeypatch.setattr(webhooks.settings, "WEBHOOK_SECRET", "secret")

    with pytest.raises(
        ValueError, match="WEBHOOK_URLS must contain only http or https URLs"
    ):
        run_deliver()


def test_deliver_posts_signed_payload(monkeypatch):
    class FakeResponse:
        raised = False

        def raise_for_status(self):
            self.raised = True

    posted = []
    response = FakeResponse()
    created = {}

    class FakeClient:
        def __init__(self, **kwargs):
            created.update(kwargs)

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_value, traceback):
            return None

        async def post(self, url, content, headers):
            posted.append((url, content, headers))
            return response

    monkeypatch.setattr(
        webhooks.settings,
        "WEBHOOK_URLS",
        "https://one.test/hook, https://two.test/hook",
    )
    monkeypatch.setattr(webhooks.settings, "WEBHOOK_SECRET", "secret")
    monkeypatch.setattr(webhooks.time, "time", lambda: 1234567890)
    monkeypatch.setattr(webhooks.httpx2, "AsyncClient", FakeClient)

    run_deliver("email.subscribed", {"email": "kyle@example.com", "id": 1})

    body = json.dumps(
        {"event": "email.subscribed", "data": {"email": "kyle@example.com", "id": 1}},
        separators=(",", ":"),
        sort_keys=True,
    ).encode()
    signature = hmac.new(b"secret", b"1234567890." + body, hashlib.sha256).hexdigest()

    assert created == {"timeout": 10}
    assert posted == [
        (
            "https://one.test/hook",
            body,
            {
                "content-type": "application/json",
                "x-webhook-event": "email.subscribed",
                "x-webhook-timestamp": "1234567890",
                "x-webhook-signature": f"sha256={signature}",
            },
        ),
        (
            "https://two.test/hook",
            body,
            {
                "content-type": "application/json",
                "x-webhook-event": "email.subscribed",
                "x-webhook-timestamp": "1234567890",
                "x-webhook-signature": f"sha256={signature}",
            },
        ),
    ]
    assert response.raised is True
