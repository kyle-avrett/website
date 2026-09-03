import anyio
import pytest

from src.services import listmonk


def run_create_subscriber():
    return anyio.run(listmonk.create_subscriber, "Kyle", "kyle@example.com", "site")


def test_create_subscriber_requires_url(monkeypatch):
    monkeypatch.setattr(listmonk.settings, "LISTMONK_URL", "")

    with pytest.raises(ValueError, match="LISTMONK_URL not set"):
        run_create_subscriber()


def test_create_subscriber_requires_list(monkeypatch):
    monkeypatch.setattr(listmonk.settings, "LISTMONK_URL", "https://listmonk.test")
    monkeypatch.setattr(listmonk.settings, "LISTMONK_LIST", 0)

    with pytest.raises(ValueError, match="LISTMONK_LIST not set"):
        run_create_subscriber()


def test_create_subscriber_rejects_invalid_url(monkeypatch):
    monkeypatch.setattr(listmonk.settings, "LISTMONK_URL", "ftp://listmonk.test")
    monkeypatch.setattr(listmonk.settings, "LISTMONK_LIST", 1)

    with pytest.raises(ValueError, match="LISTMONK_URL must be http or https"):
        run_create_subscriber()


def test_create_subscriber_posts_to_listmonk(monkeypatch):
    class FakeResponse:
        raised = False

        def raise_for_status(self):
            self.raised = True

    class FakeClient:
        posted = None
        response = FakeResponse()

        def __init__(self, **kwargs):
            self.kwargs = kwargs

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_value, traceback):
            return None

        async def post(self, url, json):
            self.__class__.posted = (url, json)
            return self.response

    monkeypatch.setattr(listmonk.settings, "LISTMONK_URL", "https://listmonk.test/")
    monkeypatch.setattr(listmonk.settings, "LISTMONK_USER", "user")
    monkeypatch.setattr(listmonk.settings, "LISTMONK_PASS", "pass")
    monkeypatch.setattr(listmonk.settings, "LISTMONK_LIST", 7)
    monkeypatch.setattr(listmonk.httpx2, "AsyncClient", FakeClient)

    run_create_subscriber()

    assert FakeClient.posted == (
        "https://listmonk.test/api/subscribers",
        {
            "name": "Kyle",
            "email": "kyle@example.com",
            "status": "enabled",
            "lists": [7],
            "attribs": {"source": "site"},
        },
    )
    assert FakeClient.response.raised is True
