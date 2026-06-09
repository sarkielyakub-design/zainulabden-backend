from pydantic import (
    BaseModel,
    EmailStr,
)

from typing import Optional


# =========================
# REGISTER
# =========================
class UserCreate(BaseModel):

    name: str

    email: EmailStr

    phone: str

    address: str

    nationality: str

    password: str


# =========================
# LOGIN
# =========================
class UserLogin(BaseModel):

    email: EmailStr

    password: str


# =========================
# RESPONSE
# =========================
class UserResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    phone: Optional[str]

    address: Optional[str]

    nationality: Optional[str]

    role: str

    is_admin: bool

    is_verified: bool

    class Config:

        from_attributes = True