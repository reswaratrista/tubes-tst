from datetime import time
from typing import List
from database.connection import Database, get_session
from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from models.movies import Movie
from models.histories import History
from sqlmodel import Session, select, update

movie_router = APIRouter(
    tags=["Movie"],
)

movie_database = Database(Movie)

@movie_router.get("/", response_model=List[Movie])
async def retrieve_all_movies(session=Depends(get_session)) -> List[Movie]:
    statement = select(Movie)
    movies = session.exec(statement).all()
    return movies

@movie_router.get("/{movieId}")
def get_movie_by_id(movieId: int, session: Session = Depends(get_session)):
    movie = session.exec(select(Movie).where(Movie.movieId == movieId)).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="User not found")
    return movie

@movie_router.post("/new")
async def create_movie(new_movie: Movie,
session=Depends(get_session)) -> dict:
    session.add(new_movie)
    session.commit()
    session.refresh(new_movie)
    return {
        "message": "Movie created successfully"
    }

@movie_router.get("/recommend")
async def get_movie_recommendations(session=Depends(get_session)):
    min_avg_watch_time: int = 0
    statement = select(Movie).where(Movie.avgWatchTime > min_avg_watch_time).order_by(Movie.avgWatchTime)
    recommended_movies = session.exec(statement).all()
    return recommended_movies

def update_avg_watch_time(session, movie_id):
    statement = select(History).where(History.movieId == movie_id)
    histories = session.exec(statement).all()
    
    total_duration = 0

    for history in histories:
        watched_duration = History.watchedDuration
        # Parse watchedDuration to seconds
        hours, minutes, seconds = map(int, str(watched_duration).split(':'))
        total_duration += hours * 3600 + minutes * 60 + seconds

    if histories:
        avg_watch_time = total_duration / len(histories)
    else:
        avg_watch_time = 0

    # Convert avg_seconds back to HH:MM:SS string format
    avg_watch_time = time(
        hours=avg_watch_time // 3600,
        minutes=(avg_watch_time % 3600) // 60,
        seconds=avg_watch_time % 60
    )

    # Convert avg_watch_time to a string in "HH:MM:SS" format
    avg_watch_time_str = avg_watch_time.strftime("%H:%M:%S")

    # Update the movie's avgWatchTime
    statement = update(Movie).where(Movie.movieId == movie_id).values(avgWatchTime=avg_watch_time_str)
    session.exec(statement)
    session.commit()