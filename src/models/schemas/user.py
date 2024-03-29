import uuid
import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator

from src.models.enums.role import UserRole


def is_valid_email(email: str) -> bool:
    pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,10}$"
    access_domain = ["milk.com", "gmail.com", "milkhunters.ru"]
    is_ok = False
    for domain in access_domain:
        if email.endswith(domain):
            is_ok = True
            break
    return (re.match(pattern, email) is not None) and is_ok


def is_valid_password(password: str) -> bool:
    pattern = r"^(?=.*[A-Z])(?=.*[\d!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$"
    return re.match(pattern, password) is not None


class User(BaseModel):
    """
    Базовая схема пользователя
    """
    id: uuid.UUID
    email: str
    avatar_id: Optional[uuid.UUID]
    first_name: str
    last_name: str
    patronymic: str
    department: str
    job_title: str
    role: UserRole

    create_at: datetime
    update_at: Optional[datetime]

    class Config:
        orm_mode = True


class UserMiddle(BaseModel):
    id: uuid.UUID
    avatar_id: Optional[uuid.UUID]
    first_name: str
    last_name: str
    patronymic: str
    department: str
    job_title: str
    role: UserRole

    class Config:
        orm_mode = True


class UserSmall(UserMiddle):
    pass


class UserSignUp(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    email: str
    password: str
    department: str
    job_title: str
    role: Optional[UserRole]

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
    email: str
    password: str


class UserUpdate(BaseModel):
    avatar_id: Optional[str]


class UserPasswordUpdate(BaseModel):
    old_password: str
    new_password: str

    @validator('new_password')
    def password_must_be_valid(cls, value):
        if not (is_valid_password(value)):
            raise ValueError("Слабый или невалидный password!")
        return value


class UserUpdateByAdmin(BaseModel):
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    patronymic: Optional[str]
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


class UserUpdateByHigh(BaseModel):
    role: Optional[UserRole]
    avatar_id: Optional[str]

    @validator('role')
    def role_must_be_valid(cls, value):
        try:
            UserRole(value)
        except ValueError:
            raise ValueError(f"Значение {value!r} инвалидное для UserRole")
        if UserRole(value) not in [UserRole.USER, UserRole.HIGH_USER]:
            raise ValueError(f"Вы можете только установить роль пользователя или high пользователя")
        return value
