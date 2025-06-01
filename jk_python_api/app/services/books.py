# Books service logic

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from app.db import models, schemas
from typing import List, Optional

async def get_book(db: AsyncSession, book_id: int) -> Optional[models.Book]:
    result = await db.execute(select(models.Book).where(models.Book.id == book_id))
    return result.scalars().first()

async def get_books(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Book]:
    result = await db.execute(select(models.Book).offset(skip).limit(limit))
    return result.scalars().all()

async def create_book(db: AsyncSession, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(**book.dict())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def update_book(db: AsyncSession, book_id: int, book: schemas.BookUpdate) -> Optional[models.Book]:
    db_book = await get_book(db, book_id)
    if not db_book:
        return None
    for field, value in book.dict(exclude_unset=True).items():
        setattr(db_book, field, value)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def delete_book(db: AsyncSession, book_id: int) -> bool:
    db_book = await get_book(db, book_id)
    if not db_book:
        return False
    await db.delete(db_book)
    await db.commit()
    return True
