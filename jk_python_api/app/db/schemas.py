# Pydantic schemas

from pydantic import BaseModel, Field
from typing import List, Optional

class ReviewBase(BaseModel):
    review_text: str
    rating: float

class ReviewCreate(ReviewBase):
    user_id: str

class ReviewRead(ReviewBase):
    id: int
    user_id: str
    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookRead(BookBase):
    id: int
    reviews: List[ReviewRead] = []
    class Config:
        orm_mode = True

from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True
