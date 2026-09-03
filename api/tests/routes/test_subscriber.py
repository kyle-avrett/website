def test_subscriber_crud(client, monkeypatch):
    created_in_listmonk = []
    sent_messages = []

    async def fake_create_subscriber(name, email, source=None):
        created_in_listmonk.append((name, email, source))

    async def fake_send_message(message, title="New subscriber"):
        sent_messages.append((message, title))

    monkeypatch.setattr(
        "src.routes.subscriber.listmonk.create_subscriber", fake_create_subscriber
    )
    monkeypatch.setattr("src.routes.subscriber.gotify.send_message", fake_send_message)

    response = client.post(
        "/api/v1/subscriber",
        json={"name": "Kyle", "email": "kyle@example.com", "source": "site"},
    )
    assert response.status_code == 200
    subscriber = response.json()
    assert subscriber["id"] == 1
    assert subscriber["name"] == "Kyle"
    assert subscriber["email"] == "kyle@example.com"
    assert subscriber["source"] == "site"
    assert subscriber["date_created"]
    assert created_in_listmonk == [("Kyle", "kyle@example.com", "site")]
    assert sent_messages == [
        ("Kyle <kyle@example.com> subscribed from site", "New subscriber")
    ]

    response = client.get("/api/v1/subscriber/1")
    assert response.status_code == 200
    assert response.json() == subscriber

    response = client.put(
        "/api/v1/subscriber/1",
        json={"name": "K", "email": "k@example.com", "source": None},
    )
    assert response.status_code == 200
    updated = response.json()
    assert updated["id"] == 1
    assert updated["name"] == "K"
    assert updated["email"] == "k@example.com"
    assert updated["source"] is None

    response = client.get("/api/v1/subscribers")
    assert response.status_code == 200
    assert response.json() == [updated]

    response = client.delete("/api/v1/subscriber/1")
    assert response.status_code == 200
    assert response.json() == updated

    response = client.get("/api/v1/subscribers")
    assert response.status_code == 200
    assert response.json() == []


def test_subscriber_not_found(client):
    assert client.get("/api/v1/subscriber/404").status_code == 404
    assert (
        client.put(
            "/api/v1/subscriber/404",
            json={"name": "No", "email": "no@example.com"},
        ).status_code
        == 404
    )
    assert client.delete("/api/v1/subscriber/404").status_code == 404
