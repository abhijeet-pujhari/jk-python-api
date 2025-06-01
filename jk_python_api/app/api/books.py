from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db import schemas
from app.db.session import get_db
from app.services import books as book_service
from app.services import llama3
from app.services import reviews as review_service
from app.core.auth import get_current_user

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=schemas.BookRead, status_code=status.HTTP_201_CREATED, summary="Add a new book", description="Add a new book to the database.")
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await book_service.create_book(db, book)

@router.get("/", response_model=List[schemas.BookRead], summary="Retrieve all books", description="Get a list of all books.")
async def read_books(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await book_service.get_books(db, skip=skip, limit=limit)

@router.get("/{book_id}", response_model=schemas.BookRead, summary="Retrieve a book by ID", description="Get a specific book by its ID.")
async def read_book(book_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    book = await book_service.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=schemas.BookRead, summary="Update a book", description="Update a book's information by its ID.")
async def update_book(book_id: int, book: schemas.BookUpdate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    updated = await book_service.update_book(db, book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a book", description="Delete a book by its ID.")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    deleted = await book_service.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return None

@router.get("/{book_id}/summary")
async def get_book_summary(book_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    book = await book_service.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    review_summary = await review_service.get_review_summary(db, book_id)
    summary = await llama3.generate_summary(book.summary or book.title)
    return {"summary": summary, **review_summary}

@router.post("/generate-summary")
async def generate_book_summary(content: str):
    summary = await llama3.generate_summary(content)
    return {"summary": summary}
