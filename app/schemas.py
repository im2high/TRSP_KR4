from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, conint, constr


# ---------- Задание 9.1 (Product) ----------
class ProductBase(BaseModel):
    title: str
    price: float = Field(ge=0)
    count: int = Field(ge=0)
    description: str


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------- Задание 11.1 (валидация User) ----------
class User(BaseModel):
    username: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = "Unknown"


# ---------- Задание 10.x / 11.2 (in-memory users) ----------
class UserIn(BaseModel):
    username: str
    age: int


class UserOut(BaseModel):
    id: int
    username: str
    age: int


# ---------- Общая модель ответа об ошибке (10.1, 10.2) ----------
class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int
    details: Optional[dict] = None
