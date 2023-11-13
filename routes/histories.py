from typing import List
from database.connection import Database, get_session
from fastapi import APIRouter, Depends, HTTPException, Request, status
from models.histories import History, newHistory
from sqlmodel import select
from routes.movies import update_avg_watch_time

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

@history_router.post("/watchMovie")
async def create_history(new_history: newHistory, session=Depends(get_session)) -> dict:
    # Create a new History object
    new_history_obj = History(
        username=new_history.username,
        movieId=new_history.movieId,
        watchedDuration=new_history.watchedDuration,
    )

    # Add and commit the new history record
    session.add(new_history_obj)
    session.commit()

    # Refresh the new history object to obtain the generated historyId
    session.refresh(new_history_obj)

    # Update the average watch time for the related movie
    update_avg_watch_time(session, new_history.movieId)

    return {
        "message": "History created successfully"
    }

@history_router.put("/{historyId}", response_model=History)
async def update_history(historyId: int, updated_history: newHistory, session=Depends(get_session)) -> History:
    history = session.get(History, historyId)
    if history is None:
        raise HTTPException(status_code=404, detail="History not found")
    
    # Update history attributes
    for key, value in updated_history.dict().items():
        setattr(history, key, value)
    
    session.commit()
    session.refresh(history)
    return history

@history_router.delete("/{historyId}", response_model=dict)
async def delete_history(historyId: int, session=Depends(get_session)) -> dict:
    history = session.get(History, historyId)
    if history is None:
        raise HTTPException(status_code=404, detail="History not found")
    
    session.delete(history)
    session.commit()
    return {"message": "History deleted successfully"}
