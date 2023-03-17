import uuid
import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator

from src.models.enums.role import UserRole


def is_valid_email(email: str) -> bool:
    pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,10}$"
    return re.match(pattern, email) is not None


def is_valid_password(password: str) -> bool:
    pattern = r"^(?=.*[A-Z])(?=.*[\d!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$"
    return re.match(pattern, password) is not None


class User(BaseModel):
    """
    Базовая схема пользователя
    """
    id: uuid.UUID
    username: str
    email: str
    role: UserRole
    create_at: datetime
    update_at: Optional[datetime]

    class Config:
        orm_mode = True


class UserSmall(BaseModel):
    id: uuid.UUID
    role: UserRole
    username: str

    class Config:
        orm_mode = True


class UserSignUp(BaseModel):
    username: str
    email: str
    password: str

    @validator('email')
    def email_must_be_valid(cls, value):
        if not is_valid_email(value):
            raise ValueError("Не валидный email")
        return value

    @validator('password')
    def password_must_be_valid(cls, value):
        if not is_valid_password(value):
            raise ValueError("Слабый или не валидный пароль")
        return value


class UserSignIn(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str]


class UserUpdateAdminMode(BaseModel):
    username: Optional[str]
    email: Optional[str]
    role: Optional[UserRole]

    @validator('email')
    def email_must_be_valid(cls, value):
        if not is_valid_email(value):
            raise ValueError("Не валидный email")
        return value

    @validator('role')
    def role_must_be_valid(cls, value):
        try:
            UserRole(value)
        except ValueError:
            raise ValueError(f"Значение {value!r} инвалидное для UserRole")
        return value
