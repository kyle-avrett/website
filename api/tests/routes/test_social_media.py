EXAMPLE_POSTS = [
    {
        "id": "cm6tcts4f0005qcwit25cis26",
        "content": "This is the first post to instagram",
        "publishDate": "2025-02-06T13:09:00.000Z",
        "releaseURL": "https://facebook.com/release/release",
        "state": "PUBLISHED",
        "integration": {
            "id": "cm6s4uyou0001i2r47pxix6z1",
            "name": "test",
            "providerIdentifier": "instagram",
            "picture": "https://uploads.gitroom.com/F6LSCD8wrrQ.jpeg",
            "type": "social",
        },
    },
    {
        "id": "cm6tcts4f0005qcwit25cis26",
        "content": "This is the second post to facebook",
        "publishDate": "2025-02-06T13:09:00.000Z",
        "releaseURL": "https://facebook.com/release2/release2",
        "state": "PUBLISHED",
        "integration": {
            "id": "cm6s4uyou0001i2r47pxix6z1",
            "name": "test2",
            "providerIdentifier": "facebook",
            "picture": "https://uploads.gitroom.com/F6LSCD8wrrQ.jpeg",
            "type": "social",
        },
    },
]


def test_social_media_notify(client, monkeypatch):
    sent = []

    async def fake_notify_social_media(title, message):
        sent.append((title, message))

    monkeypatch.setattr(
        "src.routes.social_media.gotify.notify_social_media", fake_notify_social_media
    )

    response = client.post("/api/v1/social-media/notify", json=EXAMPLE_POSTS)

    assert response.status_code == 200
    assert response.json() == {"notifications_sent": 2}
    assert sent == [
        (
            "Posted to instagram",
            "This is the first post to instagram\n\nhttps://facebook.com/release/release",
        ),
        (
            "Posted to facebook",
            "This is the second post to facebook\n\nhttps://facebook.com/release2/release2",
        ),
    ]
