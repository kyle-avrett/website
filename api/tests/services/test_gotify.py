import anyio
import pytest

from src.services import gotify


def run_send_message():
    return anyio.run(gotify.send_message, "hello", "Title")


def test_send_message_requires_url(monkeypatch):
    monkeypatch.setattr(gotify.settings, "GOTIFY_URL", "")

    with pytest.raises(ValueError, match="GOTIFY_URL not set"):
        run_send_message()


def test_send_message_requires_pass(monkeypatch):
    monkeypatch.setattr(gotify.settings, "GOTIFY_URL", "https://gotify.test")
    monkeypatch.setattr(gotify.settings, "GOTIFY_PASS", "")

    with pytest.raises(ValueError, match="GOTIFY_PASS not set"):
        run_send_message()


def test_send_message_rejects_invalid_url(monkeypatch):
    monkeypatch.setattr(gotify.settings, "GOTIFY_URL", "ftp://gotify.test")
    monkeypatch.setattr(gotify.settings, "GOTIFY_PASS", "token")

    with pytest.raises(ValueError, match="GOTIFY_URL must be http or https"):
        run_send_message()


def test_send_message_posts_to_gotify(monkeypatch):
    class FakeGotify:
        created = None
        sent = None

        def __init__(self, **kwargs):
            self.__class__.created = kwargs

        async def create_message(self, message, title):
            self.__class__.sent = (message, title)

    monkeypatch.setattr(gotify.settings, "GOTIFY_URL", "https://gotify.test/")
    monkeypatch.setattr(gotify.settings, "GOTIFY_PASS", "token")
    monkeypatch.setattr(gotify, "AsyncGotify", FakeGotify)

    run_send_message()

    assert FakeGotify.created == {
        "base_url": "https://gotify.test",
        "app_token": "token",
    }
    assert FakeGotify.sent == ("hello", "Title")
