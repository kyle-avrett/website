from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from src.services import gotify, webhooks

# ----------------------------------------------------------------------------------------


class SocialMediaRequestIntegration(BaseModel):
    id: str
    name: str
    providerIdentifier: str
    picture: str | None = None
    type: str


class SocialMediaRequest(BaseModel):
    id: str
    content: str
    publishDate: datetime
    releaseURL: str
    state: str
    integration: SocialMediaRequestIntegration


class SocialMediaResponse(BaseModel):
    notifications_sent: int


# ----------------------------------------------------------------------------------------


router = APIRouter(tags=["Social Media"])


# ----------------------------------------------------------------------------------------


@router.post(
    "/social-media/notify",
    response_model=SocialMediaResponse,
    operation_id="notify_social_media",
)
async def notify(posts: list[SocialMediaRequest]):
    # notify
    for post in posts:
        await gotify.notify_social_media(
            f"Posted to {post.integration.providerIdentifier}",
            f"{post.content}\n\n{post.releaseURL}",
        )
        await webhooks.deliver(
            "social_media.published",
            post.model_dump(mode="json"),
        )

    # return
    return SocialMediaResponse(notifications_sent=len(posts))
