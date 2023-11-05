from typing import Optional, List
from pydantic import conint
from sqlmodel import JSON, SQLModel, Field, Column

class SimilaritiesBase(BaseModel):
    movieId1: int
    movieId2: int

class SimilarityField(BaseModel):
    similarity: conint(ge=1, le=5)

class Similarity(SQLModel, table=True):
    movieId1: int = Field(default=None)
    movieId2: int = Field(default=None)
    similarity: int

    class Settings:
        name = "similarity"
