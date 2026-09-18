from src.settings import settings


def test_health_check(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "project": settings.APP_NAME}


def test_openapi_documents_outbound_webhooks(client):
    schema = client.get("/openapi.json").json()

    assert sorted(schema["webhooks"]) == ["email.subscribed", "social_media.published"]
    for event in schema["webhooks"].values():
        operation = event["post"]
        assert operation["requestBody"]["content"]["application/json"]["schema"]["$ref"]
        assert {parameter["name"] for parameter in operation["parameters"]} == {
            "x-webhook-event",
            "x-webhook-timestamp",
            "x-webhook-signature",
        }
