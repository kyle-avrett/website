"""Docs helpers for FastAPI docs, FastMCP docs, and the shared docs index."""

import asyncio
import contextlib
import html
import io
from collections.abc import Coroutine
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastmcp import FastMCP
from fastmcp_docs import FastMCPDocs
from fastmcp_docs.config import FastMCPDocsConfig

from src.settings import settings

# Shared by /docs HTML and tests; keep docs URLs visible in one place.
DOCS_SECTIONS = [
    (
        "API",
        [
            ("/docs/api", "Swagger"),
            ("/docs/api/redoc", "ReDoc"),
            ("/docs/api/openapi.json", "OpenAPI Schema"),
        ],
    ),
    (
        "MCP",
        [
            ("/mcp", "Endpoint"),
            ("/docs/mcp", "Swagger"),
            ("/mcp/tools.json", "Tools"),
            ("/docs/mcp/openapi.json", "OpenAPI Schema"),
        ],
    ),
]


def setup_mcp_docs(mcp: FastMCP) -> None:
    """Register FastMCP docs routes before the MCP ASGI app is built."""
    mcp_docs = FastMCPDocs(
        mcp=mcp,
        config=FastMCPDocsConfig(
            title=f"{settings.APP_NAME} MCP tools",
            description="Documentation for MCP tools generated from this API.",
            base_url=settings.BASE_URL,
            docs_ui_route="/docs/mcp",
            api_tools_route="/mcp/tools.json",
            api_tool_detail_route="/mcp/tools/{tool_name}",
            openapi_route="/docs/mcp/openapi.json",
            favicon_url="/favicon.ico",
            verbose=False,
        ),
    )
    run_before_http_app(mcp_docs.setup())


def run_before_http_app(coro: Coroutine[Any, Any, Any]) -> None:
    """Run async FastMCP docs setup from sync module startup.

    Uvicorn imports inside an event loop; a worker thread avoids nested asyncio.run().
    """

    def run() -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            asyncio.run(coro)

    with ThreadPoolExecutor(max_workers=1) as executor:
        executor.submit(run).result()


def register_docs_index(app: FastAPI) -> None:
    """Add the human docs index at /docs."""

    @app.get("/docs", response_class=HTMLResponse, include_in_schema=False)
    def docs_index() -> str:
        """Render a small link index styled like the sitemap XSL."""
        title = html.escape(f"{settings.APP_NAME} docs")
        section_html = "\n".join(
            "<section>"
            f"<h2>{html.escape(section_title)}</h2>"
            "<ol>"
            + "\n".join(
                f'<li><a href="{html.escape(url)}">{html.escape(label)}</a></li>'
                for url, label in links
            )
            + "</ol>"
            "</section>"
            for section_title, links in DOCS_SECTIONS
        )
        return f"""<!doctype html>
<html lang="en">
    <head>
        <title>{title}</title>
        <style>
            body {{ font-family: system-ui, sans-serif; margin: 2rem auto; max-width: 64rem; padding: 0 1rem; line-height: 1.5; }}
            a {{ color: currentColor; }}
            li {{ margin: 0.5rem 0; }}
        </style>
    </head>
    <body>
        <main>
            <h1>{title}</h1>
            {section_html}
        </main>
    </body>
</html>"""
