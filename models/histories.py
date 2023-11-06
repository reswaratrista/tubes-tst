from datetime import timedelta
from typing import List
from pydantic import BaseModel
from sqlmodel import Relationship, SQLModel, Field
class History(SQLModel, table=True):
    historyId: int = Field(default=None, primary_key=True)
    username: str = Field(default=None, foreign_key='user.username')
    movieId: int = Field(default=None, foreign_key='movie.movieId')
    watchedDuration: str
    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "historyId": 1,
                "username": "reswaratatak",
                "movieId": 3,
                "watchedDuration": "0:45:03"  # Adjust the format as needed
            }
        }
    class Settings:
        name = "histories"

class newHistory(BaseModel):
    username: str
    movieId: int
    watchedDuration: str