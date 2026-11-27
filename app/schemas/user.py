from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator

BCRYPT_MAX_BYTES = 72


def check_bcrypt_limit(value: str) -> str:
    if len(value.encode("utf-8")) > BCRYPT_MAX_BYTES:
        raise ValueError(f"password must be at most {BCRYPT_MAX_BYTES} bytes")
    return value


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def limit_password_bytes(cls, value: str) -> str:
        return check_bcrypt_limit(value)


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def limit_password_bytes(cls, value: str) -> str:
        return check_bcrypt_limit(value)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: Literal["user", "admin"]