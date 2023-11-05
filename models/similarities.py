from typing import Optional, List
from pydantic import BaseModel, conint
from sqlmodel import JSON, SQLModel, Field, Column

class SimilaritiesBase(BaseModel):
    movieId1: int
    movieId2: int

class SimilarityField(BaseModel):
    similarity: conint(ge=1, le=5)

class Similarity(SQLModel, table=True):
    movieId1: int = Field(default=None, primary_key=True, foreign_key='movie.movieId')
    movieId2: int = Field(default=None, primary_key=True, foreign_key='movie.movieId')
    similarity: int

    class Settings:
        name = "similarity"
