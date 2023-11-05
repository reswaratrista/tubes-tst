from typing import List

from database.connection import Database, get_session
from fastapi import APIRouter, Depends, HTTPException, Request, status
from models.categories import Category
from sqlmodel import select

category_router = APIRouter(
    tags=["Category"],
)

category_database = Database(Category)

@category_router.get("/", response_model=List[Category])
async def retrieve_all_events(session=Depends(get_session)) -> List[Category]:
    statement = select(Category)
    events = session.exec(statement).all()
    return events