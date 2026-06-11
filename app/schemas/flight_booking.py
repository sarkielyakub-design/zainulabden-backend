from pydantic import BaseModel
from typing import Optional


class FlightBookingCreate(BaseModel):
    airline: str

    origin: str
    destination: str

    departure_date: str
    return_date: Optional[str] = None

    first_name: str
    middle_name: Optional[str] = None
    last_name: str

    gender: str
    date_of_birth: str

    nationality: str

    passport_number: str
    passport_issue_date: str
    passport_expiry_date: str
    passport_issuing_country: str

    email: str
    phone: str

    travel_class: str

    amount: float