from typing import Optional, List
from sqlmodel import JSON, SQLModel, Field, Column
from pydantic import BaseModel, EmailStr

class User(SQLModel, table=True):
    username: str = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    password: str
    gender: bool

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "username": "reswaratristaa",
                "name": "reswara trista",
                "email" : "tatata@example.com",
                "password": "1234567890",
                "gender" : True
            }
        }

    class Settings:
        name = "users"
