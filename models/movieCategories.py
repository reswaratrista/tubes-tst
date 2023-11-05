from typing import Optional, List
from sqlmodel import JSON, SQLModel, Field, Column

class MovieCategory(SQLModel, table=True):
    categoryId: int = Field(default=None, primary_key=True, foreign_key='category.categoryId')
    movieId: int = Field(default = None, primary_key=True, foreign_key='movie.movieId')

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "categoryId": 1,
                "movieId": 2,
            }
        }

    class Settings:
        name = "movieCategories"
