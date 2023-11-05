from typing import List

from database.connection import Database, get_session
from fastapi import APIRouter, Depends, HTTPException, Request, status
from models.movieCategories import MovieCategory
from sqlmodel import select

moviecategory_router = APIRouter(
    tags=["MovieCategory"],
)

moviecategory_database = Database(MovieCategory)

@moviecategory_router.get("/", response_model=List[MovieCategory])
async def retrieve_all_events(session=Depends(get_session)) -> List[MovieCategory]:
    statement = select(MovieCategory)
    events = session.exec(statement).all()
    return events