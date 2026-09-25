from pydantic import EmailStr
from app.schemas.base import Base


class LoginRequest(Base):
    email: EmailStr
    password: str


class LoginResponse(Base):
    message: str
    email: EmailStr
