from datetime import time
from typing import Optional, List
from pydantic import BaseModel, conint
from sqlmodel import JSON, SQLModel, Field, Column

class History(SQLModel, table=True):
    username: int = Field(default=None, primary_key=True, foreign_key='user.username')
    movieId: int = Field(default=None, primary_key=True, foreign_key='movie.movieId')
    watchedDuration: time

    class Settings:
        name = "history"
