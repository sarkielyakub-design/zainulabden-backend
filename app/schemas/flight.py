from pydantic import BaseModel
from typing import Optional


class FlightSearchRequest(BaseModel):
    origin: str
    destination: str
    departure_date: str
    return_date: Optional[str] = None

    adults: int = 1
    children: int = 0
    infants: int = 0

    travel_class: str = "ECONOMY"
    trip_type: str = "round_trip"


class FlightOffer(BaseModel):
    airline: str
    flight_number: str
    departure: str
    arrival: str

    price: str
    currency: str