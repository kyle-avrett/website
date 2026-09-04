from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from src.services import gotify

# ----------------------------------------------------------------------------------------


class SocialMediaIntegration(BaseModel):
    id: str
    name: str
    providerIdentifier: str
    picture: str | None = None
    type: str


class SocialMediaPost(BaseModel):
    id: str
    content: str
    publishDate: datetime
    releaseURL: str
    state: str
    integration: SocialMediaIntegration


# ----------------------------------------------------------------------------------------

router = APIRouter(tags=["Social Media"])

# ----------------------------------------------------------------------------------------


@router.post("/social-media/notify")
async def notify_social_media(posts: list[SocialMediaPost]):
    for post in posts:
        await gotify.notify_social_media(
            f"Posted to {post.integration.providerIdentifier}",
            f"{post.content}\n\n{post.releaseURL}",
        )
    return {"notifications_sent": len(posts)}
