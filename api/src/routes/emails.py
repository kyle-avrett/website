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


class Email(Base):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    source: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    date_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


# ----------------------------------------------------------------------------------------


class EmailRequest(BaseModel):
    name: str
    email: str
    source: str | None = None


class EmailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    source: str | None = None
    date_created: datetime


# ----------------------------------------------------------------------------------------


router = APIRouter(tags=["Emails"])
Database = Annotated[AsyncSession, Depends(get_db)]


@router.post("/emails", response_model=EmailResponse)
async def create_email(request: EmailRequest, db: Database):
    # database
    email = Email(name=request.name, email=request.email, source=request.source)
    db.add(email)
    await db.commit()
    await db.refresh(email)

    # listmonk
    listmonk_subscriber = await listmonk.create_subscriber(
        email.name, email.email, email.source
    )
    await listmonk.send_welcome_email(listmonk_subscriber)

    # notify
    await gotify.notify_website(
        "New Email Subscriber",
        f"{email.name} <{email.email}> subscribed"
        + (f" from {email.source}" if email.source else ""),
    )

    # return
    return email


@router.get("/emails/{email_id}", response_model=EmailResponse)
async def read_email(email_id: int, db: Database):
    result = await db.execute(select(Email).where(Email.id == email_id))
    email = result.scalar_one_or_none()
    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    return email


@router.put("/emails/{email_id}", response_model=EmailResponse)
async def update_email(email_id: int, request: EmailRequest, db: Database):
    result = await db.execute(select(Email).where(Email.id == email_id))
    email = result.scalar_one_or_none()
    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")

    email.name = request.name
    email.email = request.email
    email.source = request.source
    await db.commit()
    await db.refresh(email)
    return email


@router.delete("/emails/{email_id}", response_model=EmailResponse)
async def delete_email(email_id: int, db: Database):
    result = await db.execute(select(Email).where(Email.id == email_id))
    email = result.scalar_one_or_none()
    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")

    await db.delete(email)
    await db.commit()
    return email


@router.get("/emails", response_model=list[EmailResponse])
async def list_emails(db: Database):
    result = await db.execute(select(Email))
    return result.scalars().all()
