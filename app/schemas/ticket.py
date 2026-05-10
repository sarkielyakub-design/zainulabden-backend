from pydantic import BaseModel
from typing import Optional
from enum import Enum


# =========================
# SEAT CLASS
# =========================
class SeatClass(str, Enum):
    economy = "Economy"
    business = "Business"
    first_class = "First Class"


# =========================
# CREATE
# =========================
class TicketCreate(BaseModel):

    airline: str

    from_airport: str

    to_airport: str

    departure_date: str

    return_date: Optional[str] = None

    price: float

    seat_class: SeatClass

    description: Optional[str] = None

    image: Optional[str] = None


# =========================
# UPDATE
# =========================
class TicketUpdate(BaseModel):

    airline: Optional[str] = None

    from_airport: Optional[str] = None

    to_airport: Optional[str] = None

    departure_date: Optional[str] = None

    return_date: Optional[str] = None

    price: Optional[float] = None

    seat_class: Optional[SeatClass] = None

    description: Optional[str] = None

    image: Optional[str] = None


# =========================
# RESPONSE
# =========================
class TicketResponse(BaseModel):

    id: int

    airline: str

    from_airport: str

    to_airport: str

    departure_date: str

    return_date: Optional[str]

    price: float

    seat_class: SeatClass

    description: Optional[str]

    image: Optional[str]

    class Config:
        from_attributes = True