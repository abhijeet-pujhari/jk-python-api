from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db import schemas
from app.db.session import get_db
from app.services import recommendations as rec_service
from app.core.auth import get_current_user

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/", response_model=List[schemas.BookRead])
async def get_recommendations(genre: str = None, min_rating: float = 0, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await rec_service.get_recommendations(db, genre, min_rating)
