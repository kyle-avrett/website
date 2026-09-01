import anyio

from src import database


class FakeSessionContext:
    def __init__(self):
        self.session = object()

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc_value, traceback):
        return None


def test_get_db_yields_session(monkeypatch):
    context = FakeSessionContext()
    monkeypatch.setattr(database, "AsyncSessionLocal", lambda: context)

    async def consume_db_session():
        sessions = []
        async for session in database.get_db():
            sessions.append(session)
        return sessions

    assert anyio.run(consume_db_session) == [context.session]
