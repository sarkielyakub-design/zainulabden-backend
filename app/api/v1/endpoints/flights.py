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
        "success": True,
        "data": [
            {
                "airline": "Qatar Airways",
                "flight_number": "QR1431",
                "departure": payload.origin,
                "arrival": payload.destination,
                "price": "350",
                "currency": "USD",
                "duration": "4h 25m"
            },
            {
                "airline": "Turkish Airlines",
                "flight_number": "TK624",
                "departure": payload.origin,
                "arrival": payload.destination,
                "price": "420",
                "currency": "USD",
                "duration": "6h 10m"
            },
            {
                "airline": "Emirates",
                "flight_number": "EK785",
                "departure": payload.origin,
                "arrival": payload.destination,
                "price": "510",
                "currency": "USD",
                "duration": "5h 40m"
            }
        ]
    }