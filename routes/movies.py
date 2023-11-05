from typing import List

from database.connection import Database, get_session
from fastapi import APIRouter, Depends, HTTPException, Request, status
from models.movies import Movie
from sqlmodel import select

movie_router = APIRouter(
    tags=["Movie"],
)

movie_database = Database(Movie)

@movie_router.get("/", response_model=List[Movie])
async def retrieve_all_events(session=Depends(get_session)) -> List[Movie]:
    statement = select(Movie)
    events = session.exec(statement).all()
    return events