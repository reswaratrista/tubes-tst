from typing import Optional, List
from sqlmodel import JSON, SQLModel, Field, Column
from pydantic import BaseModel, EmailStr
from uuid import UUID 

class User(SQLModel, table=True):
    username: str = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    password: str

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "username": "reswaratristaa",
                "name": "reswara trista",
                "email" : "tatata@example.com",
                "password": "1234567890",
            }
        }

    class Settings:
        name = "users"

class UserSignIn(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

class UpdateUser(BaseModel):
    username: str
    name: str
    email: str
    password: str