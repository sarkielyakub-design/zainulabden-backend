from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# =========================
# CREATE
# =========================
class PackageCreate(BaseModel):
    title: str = Field(..., min_length=3)
    description: str
    price: int = Field(..., gt=0)

    flight_name: Optional[str] = ""
    flight_from: Optional[str] = ""
    flight_to: Optional[str] = ""

    departure_date: Optional[str] = ""
    return_date: Optional[str] = ""

    hotel_name: Optional[str] = ""
    hotel_rating: Optional[str] = "3"

    category: Optional[str] = "standard"

    duration_days: Optional[int] = 0

    total_slots: Optional[int] = 0
    booked_slots: Optional[int] = 0

    image_url: Optional[str] = None


# =========================
# UPDATE
# =========================
class PackageUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None

    flight_name: Optional[str] = None
    flight_from: Optional[str] = None
    flight_to: Optional[str] = None

    departure_date: Optional[str] = None
    return_date: Optional[str] = None

    hotel_name: Optional[str] = None
    hotel_rating: Optional[str] = None

    category: Optional[str] = None

    duration_days: Optional[int] = None

    total_slots: Optional[int] = None
    booked_slots: Optional[int] = None

    image_url: Optional[str] = None


# =========================
# OUTPUT
# =========================
class PackageOut(BaseModel):
    id: int

    title: str
    description: str
    price: float

    flight_name: Optional[str]
    flight_from: Optional[str]
    flight_to: Optional[str]

    departure_date: Optional[str]
    return_date: Optional[str]

    hotel_name: Optional[str]
    hotel_rating: Optional[str]

    category: Optional[str]

    duration_days: Optional[int]

    total_slots: Optional[int]
    booked_slots: Optional[int]

    image_url: Optional[str]

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True