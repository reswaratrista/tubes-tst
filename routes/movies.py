from typing import List
from database.connection import Database, get_session
from fastapi import APIRouter, Depends, HTTPException, Request, status
from models.movies import Movie
from sqlmodel import Session, select

movie_router = APIRouter(
    tags=["Movie"],
)

movie_database = Database(Movie)

@movie_router.get("/", response_model=List[Movie])
async def retrieve_all_movies(session=Depends(get_session)) -> List[Movie]:
    statement = select(Movie)
    movies = session.exec(statement).all()
    return movies

@movie_router.get("/movies/{movieId}")
def get_movie_by_id(movieId: int, session: Session = Depends(get_session)):
    user = session.exec(select(Movie).where(Movie.movieId == movieId)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@movie_router.post("/newMovie")
async def create_movie(new_movie: Movie,
session=Depends(get_session)) -> dict:
    session.add(new_movie)
    session.commit()
    session.refresh(new_movie)
    return {
        "message": "Movie created successfully"
}
