import anyio
import pytest

from src.services import listmonk


def run_create_subscriber():
    return anyio.run(listmonk.create_subscriber, "Kyle", "kyle@example.com", "site")


def run_send_welcome_email(listmonk_subscriber):
    return anyio.run(listmonk.send_welcome_email, listmonk_subscriber)


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

        def json(self):
            return {"data": {"id": 3, "name": "Kyle", "email": "kyle@example.com"}}

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

    listmonk_subscriber = run_create_subscriber()

    assert listmonk_subscriber == listmonk.ListmonkSubscriber(
        id=3, name="Kyle", email="kyle@example.com"
    )
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


def test_send_welcome_email_requires_template(monkeypatch):
    monkeypatch.setattr(listmonk.settings, "LISTMONK_TEMPLATE_WELCOME_EMAIL", 0)

    with pytest.raises(ValueError, match="LISTMONK_TEMPLATE_WELCOME_EMAIL not set"):
        run_send_welcome_email(
            listmonk.ListmonkSubscriber(id=3, name="Kyle", email="kyle@example.com")
        )


def test_send_welcome_email_posts_to_listmonk(monkeypatch):
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
    monkeypatch.setattr(listmonk.settings, "LISTMONK_TEMPLATE_WELCOME_EMAIL", 5)
    monkeypatch.setattr(listmonk.httpx2, "AsyncClient", FakeClient)

    run_send_welcome_email(
        listmonk.ListmonkSubscriber(id=3, name="Kyle", email="kyle@example.com")
    )

    assert FakeClient.posted == (
        "https://listmonk.test/api/tx",
        {"subscriber_id": 3, "template_id": 5},
    )
    assert FakeClient.response.raised is True
