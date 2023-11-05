from typing import List

from database.connection import Database, get_session
from fastapi import APIRouter, Depends, HTTPException, Request, status
from models.similarities import Similarity
from sqlmodel import select

movie_router = APIRouter(
    tags=["Similarity"],
)

movie_database = Database(Similarity)

@movie_router.get("/", response_model=List[Similarity])
async def retrieve_all_events(session=Depends(get_session)) -> List[Similarity]:
    statement = select(Similarity)
    events = session.exec(statement).all()
    return events