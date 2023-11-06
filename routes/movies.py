from typing import List
from database.connection import Database, get_session
from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from models.movies import Movie
from models.histories import History
from sqlmodel import Session, select

movie_router = APIRouter(
    tags=["Movie"],
)

history_router = APIRouter(
    tags=["History"]
)

movie_database = Database(Movie)

@movie_router.get("/", response_model=List[Movie])
async def retrieve_all_movies(session=Depends(get_session)) -> List[Movie]:
    statement = select(Movie)
    movies = session.exec(statement).all()
    return movies

@movie_router.get("/{movieId}")
def get_movie_by_id(movieId: int, session: Session = Depends(get_session)):
    user = session.exec(select(Movie).where(Movie.movieId == movieId)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@movie_router.post("/new")
async def create_movie(new_movie: Movie,
session=Depends(get_session)) -> dict:
    session.add(new_movie)
    session.commit()
    session.refresh(new_movie)
    return {
        "message": "Movie created successfully"
}

movie_router = APIRouter(
    tags=["Movie"],
)

movie_database = Database(Movie)

@movie_router.get("/recommendation", response_model=List[Movie])
async def retrieve_all_movies(
    min_duration: str = Query("01:30:00"),  # Minimum duration for recommendations
    session=Depends(get_session)
) -> List[Movie]:
    # Calculate movie recommendations
    recommendations = get_movie_recommendations(session, min_duration)

    # Query all movies
    statement = select(Movie)
    movies = session.exec(statement).all()

    # Add recommendations to the movie objects
    movies_with_recommendations = []
    for movie in movies:
        movie_with_recommendations = movie.dict()
        movie_id = movie.movieId
        if movie_id in recommendations:
            movie_with_recommendations["recommendation"] = recommendations[movie_id]
        else:
            movie_with_recommendations["recommendation"] = None
        movies_with_recommendations.append(movie_with_recommendations)

    return movies_with_recommendations

def get_movie_recommendations(session: Session, min_duration: str):
    # Create a dictionary to store movie recommendations
    recommendations = {}

    # Query the history to calculate average watch duration for each movie
    statement = select(History)
    history_entries = session.exec(statement).all()

    movie_durations = {}  # To store total watch durations for each movie
    movie_counts = {}  # To store the number of times each movie was watched

    for entry in history_entries:
        movie_id = entry.movieId
        watched_duration = entry.watchedDuration

        if movie_id not in movie_durations:
            movie_durations[movie_id] = 0
            movie_counts[movie_id] = 0

        # Calculate total watch duration and count
        movie_durations[movie_id] += int(watched_duration.total_seconds())
        movie_counts[movie_id] += 1

    # Calculate the average watch duration for each movie
    for movie_id, duration in movie_durations.items():
        count = movie_counts[movie_id]
        if count > 0:
            average_duration_seconds = duration // count
            average_duration = f"{average_duration_seconds // 3600:02d}:{(average_duration_seconds // 60) % 60:02d}:{average_duration_seconds % 60:02d}"
            recommendations[movie_id] = average_duration

    return recommendations
