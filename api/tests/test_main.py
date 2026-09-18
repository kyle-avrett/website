import anyio
from fastmcp.client import Client

from src.main import mcp
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


def test_mcp_exposes_llm_friendly_tools(client):
    assert client.post("/mcp", json={}).status_code == 400

    async def list_tool_names() -> list[str]:
        async with Client(mcp) as mcp_client:
            return sorted(tool.name for tool in await mcp_client.list_tools())

    assert anyio.run(list_tool_names) == [
        "create_item",
        "delete_item",
        "health_check",
        "list_items",
        "notify_social_media",
        "read_item",
        "subscribe_email",
        "update_item",
    ]
