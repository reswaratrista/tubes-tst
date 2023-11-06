from typing import Optional, List
from sqlmodel import JSON, SQLModel, Field, Column
from pydantic import BaseModel, EmailStr
from datetime import time

class Movie(SQLModel, table=True):
    movieId: int = Field(default=None, primary_key=True)
    movieName: str
    duration: time
    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "movieId": 1,
                "name": "the notebook",
                "duration" : "01:16:32",
            }
        }

    def __str__(self):
        return self.watchedDuration.isoformat()
        
    class Settings:
        name = "movies"

        