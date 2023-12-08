from pydantic import BaseModel
from sqlmodel import SQLModel, Field
class History(SQLModel, table=True):
    historyId: int = Field(default=None, primary_key=True)
    username: str = Field(default=None, foreign_key='user.username')
    movieName: str = Field(default=None, foreign_key='movie.movieName')
    watchedDuration: str 
    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "historyId": 1,
                "username": "reswaratatak",
                "movieName": "The Conjuring",
                "watchedDuration": "0:45:03" 
            }
        }
    class Settings:
        name = "histories"

class newHistory(BaseModel):
    username: str
    movieName: str
    watchedDuration: str