import anyio
import pytest

from src.services import gotify


def run_notify_website():
    return anyio.run(gotify.notify_website, "Title", "hello")


def run_notify_social_media():
    return anyio.run(gotify.notify_social_media, "Title", "hello")


def test_notify_website_requires_url(monkeypatch):
    monkeypatch.setattr(gotify.settings, "GOTIFY_URL", "")

    with pytest.raises(ValueError, match="GOTIFY_URL not set"):
        run_notify_website()


def test_notify_website_requires_pass(monkeypatch):
    monkeypatch.setattr(gotify.settings, "GOTIFY_URL", "https://gotify.test")
    monkeypatch.setattr(gotify.settings, "GOTIFY_TOKEN_WEBSITE", "")

    with pytest.raises(ValueError, match="GOTIFY_TOKEN_WEBSITE not set"):
        run_notify_website()


def test_notify_website_rejects_invalid_url(monkeypatch):
    monkeypatch.setattr(gotify.settings, "GOTIFY_URL", "ftp://gotify.test")
    monkeypatch.setattr(gotify.settings, "GOTIFY_TOKEN_WEBSITE", "token")

    with pytest.raises(ValueError, match="GOTIFY_URL must be http or https"):
        run_notify_website()


def test_notify_website_posts_to_gotify(monkeypatch):
    class FakeGotify:
        created = None
        sent = None

        def __init__(self, **kwargs):
            self.__class__.created = kwargs

        async def create_message(self, message, title):
            self.__class__.sent = (message, title)

    monkeypatch.setattr(gotify.settings, "GOTIFY_URL", "https://gotify.test/")
    monkeypatch.setattr(gotify.settings, "GOTIFY_TOKEN_WEBSITE", "token")
    monkeypatch.setattr(gotify, "AsyncGotify", FakeGotify)

    run_notify_website()

    assert FakeGotify.created == {
        "base_url": "https://gotify.test",
        "app_token": "token",
    }
    assert FakeGotify.sent == ("hello", "Title")


def test_notify_social_media_requires_token(monkeypatch):
    monkeypatch.setattr(gotify.settings, "GOTIFY_URL", "https://gotify.test")
    monkeypatch.setattr(gotify.settings, "GOTIFY_TOKEN_SOCIAL_MEDIA", "")

    with pytest.raises(ValueError, match="GOTIFY_TOKEN_SOCIAL_MEDIA not set"):
        run_notify_social_media()


def test_notify_social_media_posts_to_gotify(monkeypatch):
    class FakeGotify:
        created = None
        sent = None

        def __init__(self, **kwargs):
            self.__class__.created = kwargs

        async def create_message(self, message, title):
            self.__class__.sent = (message, title)

    monkeypatch.setattr(gotify.settings, "GOTIFY_URL", "https://gotify.test/")
    monkeypatch.setattr(gotify.settings, "GOTIFY_TOKEN_SOCIAL_MEDIA", "social-token")
    monkeypatch.setattr(gotify, "AsyncGotify", FakeGotify)

    run_notify_social_media()

    assert FakeGotify.created == {
        "base_url": "https://gotify.test",
        "app_token": "social-token",
    }
    assert FakeGotify.sent == ("hello", "Title")
