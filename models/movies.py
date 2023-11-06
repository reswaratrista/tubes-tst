from typing import Optional, List
from sqlmodel import JSON, Relationship, SQLModel, Field, Column
from pydantic import BaseModel, EmailStr
from models.histories import History

class Movie(SQLModel, table=True):
    movieId: int = Field(default=None, primary_key=True)
    movieName: str
    duration: str
    avgWatchTime: str
    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "movieId": 1,
                "movieName": "the notebook",
                "duration" : "01:16:32",
                "avgWatchTime" : "00:00:00",
            }
        }
        


    class Settings:
        name = "movies"

        