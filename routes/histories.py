from typing import List
from database.connection import Database, get_session
from fastapi import APIRouter, Depends, HTTPException, Request, status
from models.histories import History
from sqlmodel import select

history_router = APIRouter(
    tags=["History"],
)

history_database = Database(History)

@history_router.get("/", response_model=List[History])
async def retrieve_all_histories(session=Depends(get_session)) -> List[History]:
    statement = select(History)
    histories = session.exec(statement).all()
    return histories

@history_router.get("/{movieId}", response_model=History)
async def retrieve_all_history(movie_id: int, session=Depends(get_session)) -> History:
    history = session.get(History, movie_id)
    if history is None:
        raise HTTPException(status_code=404, detail="History not found")
    return history

@history_router.post("/new")
async def create_movie(new_history: History,
session=Depends(get_session)) -> dict:
    session.add(new_history)
    session.commit()
    session.refresh(new_history)
    return {
        "message": "History created successfully"
}

