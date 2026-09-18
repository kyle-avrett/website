import anyio
from fastmcp.client import Client

from src.main import mcp
from src.settings import settings


def test_health_check(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "project": settings.APP_NAME}


def test_openapi_documents_outbound_webhooks(client):
    schema = client.get("/docs/api/openapi.json").json()

    assert sorted(schema["webhooks"]) == ["email.subscribed", "social_media.published"]
    for event in schema["webhooks"].values():
        operation = event["post"]
        assert operation["requestBody"]["content"]["application/json"]["schema"]["$ref"]
        assert {parameter["name"] for parameter in operation["parameters"]} == {
            "x-webhook-event",
            "x-webhook-timestamp",
            "x-webhook-signature",
        }


def test_docs_index_links_to_api_and_mcp_docs(client):
    response = client.get("/docs")

    assert response.status_code == 200
    assert "<h2>API</h2>" in response.text
    assert 'href="/docs/api"' in response.text
    assert 'href="/docs/api/redoc"' in response.text
    assert 'href="/docs/api/openapi.json"' in response.text

    assert "<h2>MCP</h2>" in response.text
    assert 'href="/mcp"' in response.text
    assert 'href="/docs/mcp"' in response.text
    assert 'href="/mcp/tools.json"' in response.text
    assert 'href="/docs/mcp/openapi.json"' in response.text
    assert "font-family: system-ui, sans-serif" in response.text
    assert client.get("/openapi.json").status_code == 404


def test_mcp_exposes_llm_friendly_tools(client):
    assert client.post("/mcp", json={}).status_code == 400
    docs_response = client.get("/docs/mcp")
    tools_response = client.get("/mcp/tools.json")

    assert docs_response.status_code == 200
    assert "MCP tools" in docs_response.text
    assert tools_response.status_code == 200
    assert client.get("/docs/mcp/openapi.json").status_code == 200
    assert client.get("/mcp-docs").status_code == 404

    expected_tools = [
        "create_item",
        "delete_item",
        "health_check",
        "list_items",
        "notify_social_media",
        "read_item",
        "subscribe_email",
        "update_item",
    ]
    assert sorted(tools_response.json()["tools"]) == expected_tools

    async def list_tool_names() -> list[str]:
        async with Client(mcp) as mcp_client:
            return sorted(tool.name for tool in await mcp_client.list_tools())

    assert anyio.run(list_tool_names) == expected_tools
