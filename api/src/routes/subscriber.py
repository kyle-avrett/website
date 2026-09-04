from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import DateTime, String

from src.database import Base, get_db
from src.services import gotify, listmonk

# ----------------------------------------------------------------------------------------


class Subscriber(Base):
    __tablename__ = "subscribers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    source: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    date_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


# ----------------------------------------------------------------------------------------


class SubscriberRequest(BaseModel):
    name: str
    email: str
    source: str | None = None


class SubscriberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    source: str | None = None
    date_created: datetime


# ----------------------------------------------------------------------------------------


router = APIRouter(tags=["Subscriber"])
Database = Annotated[AsyncSession, Depends(get_db)]


@router.post("/subscriber", response_model=SubscriberResponse)
async def create_subscriber(request: SubscriberRequest, db: Database):
    # database
    subscriber = Subscriber(
        name=request.name, email=request.email, source=request.source
    )
    db.add(subscriber)
    await db.commit()
    await db.refresh(subscriber)

    # listmonk
    listmonk_subscriber = await listmonk.create_subscriber(
        subscriber.name, subscriber.email, subscriber.source
    )
    await listmonk.send_welcome_email(listmonk_subscriber)

    # notify
    await gotify.notify_website(
        f"{subscriber.name} <{subscriber.email}> subscribed"
        + (f" from {subscriber.source}" if subscriber.source else "")
    )

    # return
    return subscriber


@router.get("/subscriber/{subscriber_id}", response_model=SubscriberResponse)
async def read_subscriber(subscriber_id: int, db: Database):
    result = await db.execute(select(Subscriber).where(Subscriber.id == subscriber_id))
    subscriber = result.scalar_one_or_none()
    if subscriber is None:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return subscriber


@router.put("/subscriber/{subscriber_id}", response_model=SubscriberResponse)
async def update_subscriber(
    subscriber_id: int, request: SubscriberRequest, db: Database
):
    result = await db.execute(select(Subscriber).where(Subscriber.id == subscriber_id))
    subscriber = result.scalar_one_or_none()
    if subscriber is None:
        raise HTTPException(status_code=404, detail="Subscriber not found")

    subscriber.name = request.name
    subscriber.email = request.email
    subscriber.source = request.source
    await db.commit()
    await db.refresh(subscriber)
    return subscriber


@router.delete("/subscriber/{subscriber_id}", response_model=SubscriberResponse)
async def delete_subscriber(subscriber_id: int, db: Database):
    result = await db.execute(select(Subscriber).where(Subscriber.id == subscriber_id))
    subscriber = result.scalar_one_or_none()
    if subscriber is None:
        raise HTTPException(status_code=404, detail="Subscriber not found")

    await db.delete(subscriber)
    await db.commit()
    return subscriber


@router.get("/subscribers", response_model=list[SubscriberResponse])
async def list_subscribers(db: Database):
    result = await db.execute(select(Subscriber))
    return result.scalars().all()
