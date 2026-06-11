from pydantic import BaseModel
from typing import Optional
from datetime import date


class FlightSearchRequest(BaseModel):
    origin: str
    destination: str

    departure_date: date
    return_date: Optional[date] = None

    adults: int = 1
    children: int = 0
    infants: int = 0

    travel_class: str = "ECONOMY"
    trip_type: str = "round_trip"