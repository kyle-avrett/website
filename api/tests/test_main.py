from src.settings import settings


def test_health_check(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "project": settings.APP_NAME}


def test_cors_allows_site_origin(client):
    response = client.options(
        "/api/v1/subscriber",
        headers={
            "Origin": "https://kyleavrett.com",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "https://kyleavrett.com"
