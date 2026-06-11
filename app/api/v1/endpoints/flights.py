from fastapi import APIRouter
from app.schemas.flight import FlightSearchRequest

router = APIRouter(
    prefix="/flights",
    tags=["Flights"]
)

@router.post("/search")
async def search_flights(
    payload: FlightSearchRequest
):
    return {
        "origin": payload.origin,
        "destination": payload.destination,
        "departure_date": payload.departure_date,
        "return_date": payload.return_date,
        "adults": payload.adults,
        "children": payload.children,
        "infants": payload.infants,
        "travel_class": payload.travel_class,
        "trip_type": payload.trip_type,
        "message": "Flight search received successfully"
    }