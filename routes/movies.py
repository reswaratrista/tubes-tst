from database.connection import Database
from fastapi import APIRouter, HTTPException, status
from models.movies import Movie

movie_router = APIRouter(
    tags=["Movie"],
)

movie_database = Database(Movie)