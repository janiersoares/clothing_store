from typing import Annotated

import psycopg
from fastapi import APIRouter, Depends, HTTPException, status

from app.db.connection import get_db
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.user_service import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    authenticate_user,
    register_user,
)

DbConnection = Annotated[psycopg.Connection, Depends(get_db)]

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, connection: DbConnection) -> dict:
    try:
        user = register_user(connection, data.email, data.password)
    except EmailAlreadyExistsError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    return user


@router.post("/login", response_model=UserOut)
def login(data: UserLogin, connection: DbConnection) -> dict:
    try:
        user = authenticate_user(connection, data.email, data.password)
    except InvalidCredentialsError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error)) from error
    return user