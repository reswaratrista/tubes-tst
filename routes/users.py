from typing import Union, Any
from datetime import datetime
from jose import jwt
from pydantic import ValidationError
from sqlmodel import Session, select
from database.connection import Database, get_session
from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from models.users import User, Token, TokenPayload

from routes.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password,
)
from routes.utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)

user_router = APIRouter(
    tags=["User"],
)

user_database = Database(User)

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="user/login",
    scheme_name="JWT"
)

async def get_current_user(token: str = Depends(reuseable_oauth), session: Session = Depends(get_session)) -> dict:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = session.exec(select(User).where(User.email == token_data.sub)).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return user

@user_router.get('/me', summary='Get details of currently logged in user', response_model=User)
async def get_me(user: User = Depends(get_current_user)):
    return user

@user_router.get("/{username}")
def get_user_by_username(username: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.post("/register")
def sign_user_up(user: User, session: Session = Depends(get_session)) -> dict:
    user_exist =  session.exec(select(User).where(User.username == user.username)).first()

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with username provided exists already."
        )

    new_user_obj = User(
        email=user.email,
        username=user.username,
        password=get_hashed_password(user.password),
        name=user.name
    )


    session.add(new_user_obj)
    session.commit()


    session.refresh(new_user_obj)

    return {
        "message": "Successfully created user"
    }

@user_router.post('/login', summary="Create access and refresh tokens for user", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
) -> dict:
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if user is None or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    
    return {
        "access_token": create_access_token(user.email),
        "token_type": "bearer"
    }