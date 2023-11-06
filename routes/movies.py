from datetime import time
from typing import List
from database.connection import Database, get_session
from fastapi import APIRouter, Depends, HTTPException
from models.movies import Movie, MovieUpdate, newMovie
from models.histories import History
from sqlmodel import Session, select, update

movie_router = APIRouter(
    tags=["Movie"],
)

movie_database = Database(Movie)
history_database = Database(History)

@movie_router.get("/", response_model=List[Movie])
async def retrieve_all_movies(session=Depends(get_session)) -> List[Movie]:
    statement = select(Movie)
    movies = session.exec(statement).all()
    return movies

@movie_router.get("/recommend")
async def get_movie_recommendations(session=Depends(get_session)):
    min_avg_watch_time: int = 0
    statement = select(Movie).where(Movie.avgWatchTime > min_avg_watch_time).order_by(Movie.avgWatchTime)
    recommended_movies = session.exec(statement).all()
    return recommended_movies

@movie_router.get("/{movieId}")
def get_movie_by_id(movieId: int, session: Session = Depends(get_session)):
    movie = session.exec(select(Movie).where(Movie.movieId == movieId)).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="User not found")
    return movie

@movie_router.post("/new")
async def create_movie(new_movie: newMovie, session=Depends(get_session)) -> dict:
    # Create a new Movie object
    new_movie_obj = Movie(
        movieName=new_movie.movieName,
        duration=new_movie.duration,
        avgWatchTime="00:00:00",  # Initialize with 00:00:00
    )

    # Add and commit the new movie record
    session.add(new_movie_obj)
    session.commit()

    # Refresh the new movie object to obtain the generated movieId
    session.refresh(new_movie_obj)

    return {
        "message": "Movie created successfully"
    }



def update_avg_watch_time(session, movie_id):
    statement = select(History).where(History.movieId == movie_id)
    histories = session.exec(statement).all()

    total_duration = 0

    for history in histories:
        watched_duration = history.watchedDuration
        # Parse watchedDuration to seconds
        hours, minutes, seconds = map(int, str(watched_duration).split(':'))
        total_duration += hours * 3600 + minutes * 60 + seconds

    if histories:
        avg_watch_time = total_duration // len(histories)
    else:
        avg_watch_time = 0

    # Convert avg_seconds back to HH:MM:SS string format
    avg_watch_time = time(
        hour=avg_watch_time // 3600,
        minute=(avg_watch_time % 3600) // 60,
        second=avg_watch_time % 60
    )

    # Convert avg_watch_time to a string in "HH:MM:SS" format
    avg_watch_time_str = avg_watch_time.strftime("%H:%M:%S")

    # Update the movie's avgWatchTime
    statement = update(Movie).where(Movie.movieId == movie_id).values(avgWatchTime=avg_watch_time_str)
    session.exec(statement)
    session.commit()

@movie_router.put("/{movie_id}", response_model=Movie)
async def update_movie(movie_id: int, movie_update: MovieUpdate, session=Depends(get_session)) -> Movie:
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Update the movie fields
    for key, value in movie_update.dict(exclude_unset=True).items():
        setattr(movie, key, value)

    session.commit()
    session.refresh(movie)
    
    return movie

@movie_router.delete("/{movieId}", response_model=dict)
async def delete_movie(movieId: int, session=Depends(get_session)) -> dict:
    movie = session.get(Movie, movieId)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    session.delete(movie)
    session.commit()
    return {"message": "Movie deleted successfully"}

