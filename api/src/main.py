"""Compose the public ASGI app from REST routes, MCP routes, and docs routes."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP

from src.docs import register_docs_index, setup_mcp_docs
from src.routes.emails import router as emails_router
from src.routes.item import router as item_router
from src.routes.social_media import router as social_media_router
from src.services import webhooks
from src.settings import settings

# Keep the REST API isolated so FastMCP can read only the real API routes.

api_app = FastAPI(
    title=settings.APP_NAME, docs_url=None, redoc_url=None, openapi_url=None
)


# These routes become both REST endpoints and generated MCP tools.
api_app.include_router(item_router, prefix="/api/v1")
api_app.include_router(social_media_router, prefix="/api/v1")
api_app.include_router(emails_router, prefix="/api/v1")


# Webhook docs stay on the REST OpenAPI schema; they are outbound events.
webhooks.register(api_app)


@api_app.get("/", operation_id="health_check")
def health_check():
    """Lightweight probe for load balancers and uptime checks."""
    return {"status": "healthy", "project": settings.APP_NAME}


# FastMCP generates tool definitions from the REST API OpenAPI schema.
mcp = FastMCP.from_fastapi(app=api_app, name=f"{settings.APP_NAME} MCP")
setup_mcp_docs(mcp)
mcp_app = mcp.http_app(path="/mcp")

# The public app serves FastMCP first, then falls through to REST routes.

app = FastAPI(
    title=settings.APP_NAME,
    docs_url="/docs/api",
    redoc_url="/docs/api/redoc",
    openapi_url="/docs/api/openapi.json",
    routes=[*mcp_app.routes, *api_app.routes],
    lifespan=mcp_app.lifespan,
    webhooks=api_app.webhooks,
)
# Test fixtures override dependencies on app; share that mapping with copied REST routes.
api_app.dependency_overrides = app.dependency_overrides
register_docs_index(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGIN_LIST,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
