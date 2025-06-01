# Test cases for books

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Book
from app.services import books as book_service
from app.db import schemas

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="module")
async def db_session():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
    await engine.dispose()

@pytest.mark.asyncio
async def test_create_and_get_book(db_session):
    book_in = schemas.BookCreate(title="Test Book", author="Author", genre="Fiction", year_published=2024)
    book = await book_service.create_book(db_session, book_in)
    assert book.id is not None
    fetched = await book_service.get_book(db_session, book.id)
    assert fetched.title == "Test Book"

@pytest.mark.asyncio
async def test_update_book(db_session):
    book_in = schemas.BookCreate(title="Old Title", author="A", genre="Fiction", year_published=2023)
    book = await book_service.create_book(db_session, book_in)
    update = schemas.BookUpdate(title="New Title", author="A", genre="Fiction", year_published=2023)
    updated = await book_service.update_book(db_session, book.id, update)
    assert updated.title == "New Title"

@pytest.mark.asyncio
async def test_delete_book(db_session):
    book_in = schemas.BookCreate(title="Delete Me", author="A", genre="Fiction", year_published=2022)
    book = await book_service.create_book(db_session, book_in)
    deleted = await book_service.delete_book(db_session, book.id)
    assert deleted is True
    missing = await book_service.get_book(db_session, book.id)
    assert missing is None

@pytest.mark.asyncio
async def test_get_books(db_session):
    # Clean slate
    books = await book_service.get_books(db_session)
    for b in books:
        await book_service.delete_book(db_session, b.id)
    # Add two books
    await book_service.create_book(db_session, schemas.BookCreate(title="B1", author="A1", genre="G1", year_published=2020))
    await book_service.create_book(db_session, schemas.BookCreate(title="B2", author="A2", genre="G2", year_published=2021))
    all_books = await book_service.get_books(db_session)
    assert len(all_books) == 2

@pytest.mark.asyncio
async def test_update_nonexistent_book(db_session):
    update = schemas.BookUpdate(title="Ghost", author="Nobody", genre="None", year_published=2000)
    result = await book_service.update_book(db_session, 9999, update)
    assert result is None

@pytest.mark.asyncio
async def test_delete_nonexistent_book(db_session):
    result = await book_service.delete_book(db_session, 9999)
    assert result is False

@pytest.mark.asyncio
async def test_get_book_invalid_id(db_session):
    result = await book_service.get_book(db_session, 9999)
    assert result is None

@pytest.mark.asyncio
async def test_get_books_pagination(db_session):
    # Add 5 books
    for i in range(5):
        await book_service.create_book(db_session, schemas.BookCreate(title=f"Book{i}", author="A", genre="G", year_published=2020+i))
    books = await book_service.get_books(db_session, skip=2, limit=2)
    assert len(books) == 2
