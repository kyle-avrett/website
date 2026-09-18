from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP

from src.routes.emails import router as emails_router
from src.routes.item import router as item_router
from src.routes.social_media import router as social_media_router
from src.services import webhooks
from src.settings import settings

api_app = FastAPI(
    title=settings.APP_NAME, docs_url=None, redoc_url=None, openapi_url=None
)


# routes
api_app.include_router(item_router, prefix="/api/v1")
api_app.include_router(social_media_router, prefix="/api/v1")
api_app.include_router(emails_router, prefix="/api/v1")


# webhooks
webhooks.register(api_app)


@api_app.get("/", operation_id="health_check")
def health_check():
    return {"status": "healthy", "project": settings.APP_NAME}


mcp = FastMCP.from_fastapi(app=api_app, name=f"{settings.APP_NAME} MCP")
mcp_app = mcp.http_app(path="/mcp")

app = FastAPI(
    title=settings.APP_NAME,
    routes=[*mcp_app.routes, *api_app.routes],
    lifespan=mcp_app.lifespan,
    webhooks=api_app.webhooks,
)
api_app.dependency_overrides = app.dependency_overrides


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGIN_LIST,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
