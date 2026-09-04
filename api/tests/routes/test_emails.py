from src.services import listmonk


def test_email_crud(client, monkeypatch):
    created_in_listmonk = []
    sent_welcome_emails = []
    sent_messages = []

    async def fake_create_subscriber(name, email, source=None):
        created_in_listmonk.append((name, email, source))
        return listmonk.ListmonkSubscriber(id=3, name=name, email=email)

    async def fake_send_welcome_email(listmonk_subscriber):
        sent_welcome_emails.append(listmonk_subscriber)

    async def fake_notify_website(title, message):
        sent_messages.append((title, message))

    monkeypatch.setattr(
        "src.routes.emails.listmonk.create_subscriber", fake_create_subscriber
    )
    monkeypatch.setattr(
        "src.routes.emails.listmonk.send_welcome_email", fake_send_welcome_email
    )
    monkeypatch.setattr("src.routes.emails.gotify.notify_website", fake_notify_website)

    response = client.post(
        "/api/v1/emails/subscribe",
        json={"name": "Kyle", "email": "kyle@example.com", "source": "site"},
    )
    assert response.status_code == 200
    email = response.json()
    assert email["id"] == 1
    assert email["name"] == "Kyle"
    assert email["email"] == "kyle@example.com"
    assert email["source"] == "site"
    assert email["date_created"]
    assert created_in_listmonk == [("Kyle", "kyle@example.com", "site")]
    assert sent_welcome_emails == [
        listmonk.ListmonkSubscriber(id=3, name="Kyle", email="kyle@example.com")
    ]
    assert sent_messages == [
        ("New Email Subscriber", "Kyle <kyle@example.com> subscribed from site")
    ]
