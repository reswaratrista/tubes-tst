from typing import Optional, List
from sqlmodel import JSON, SQLModel, Field, Column

class Category(SQLModel, table=True):
    categoryId: int = Field(default=None, primary_key=True)
    categoryName: str

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "categoryId": 1,
                "categoryName": "horror",
            }
        }

    class Settings:
        name = "categories"
