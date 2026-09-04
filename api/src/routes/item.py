from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String

from src.database import Base, get_db

# ----------------------------------------------------------------------------------------


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)


# ----------------------------------------------------------------------------------------


class ItemRequest(BaseModel):
    name: str | None = None


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str | None = None


# ----------------------------------------------------------------------------------------


router = APIRouter(tags=["Item"])
Database = Annotated[AsyncSession, Depends(get_db)]


# ----------------------------------------------------------------------------------------


@router.post("/item", response_model=ItemResponse)
async def create_item(request: ItemRequest, db: Database):
    item = Item(name=request.name)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.get("/item/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: Database):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/item/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, request: ItemRequest, db: Database):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    item.name = request.name
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/item/{item_id}", response_model=ItemResponse)
async def delete_item(item_id: int, db: Database):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    await db.delete(item)
    await db.commit()
    return item


@router.get("/items", response_model=list[ItemResponse])
async def list_items(db: Database):
    result = await db.execute(select(Item))
    return result.scalars().all()
