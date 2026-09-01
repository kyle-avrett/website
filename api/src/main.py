from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.item import router as item_router
from src.settings import settings

# fast api app
app = FastAPI(title=settings.APP_NAME)


# middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# routes
app.include_router(item_router, prefix="/api/v1")


@app.get("/")
def health_check():
    return {"status": "healthy", "project": settings.APP_NAME}
