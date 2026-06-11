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
        "total": 12,
        "data": [
            {
                "airline": "Qatar Airways",
                "flight_number": "QR1431",
                "departure": payload.origin,
                "arrival": payload.destination,
                "price": "350",
                "currency": "USD",
                "duration": "4h 25m",
                "stops": "Direct",
                "baggage": "23kg"
            },
            {
                "airline": "Turkish Airlines",
                "flight_number": "TK624",
                "departure": payload.origin,
                "arrival": payload.destination,
                "price": "420",
                "currency": "USD",
                "duration": "6h 10m",
                "stops": "1 Stop",
                "baggage": "30kg"
            },
            {
                "airline": "Emirates",
                "flight_number": "EK785",
                "departure": payload.origin,
                "arrival": payload.destination,
                "price": "510",
                "currency": "USD",
                "duration": "5h 40m",
                "stops": "Direct",
                "baggage": "35kg"
            },
            {
                "airline": "Saudi Airlines",
                "flight_number": "SV402",
                "departure": payload.origin,
                "arrival": payload.destination,
                "price": "390",
                "currency": "USD",
                "duration": "5h 05m",
                "stops": "Direct",
                "baggage": "25kg"
            },
            {
                "airline": "Ethiopian Airlines",
                "flight_number": "ET912",
                "departure": payload.origin,
                "arrival": payload.destination,
                "price": "330",
                "currency": "USD",
                "duration": "6h 45m",
                "stops": "1 Stop",
                "baggage": "23kg"
            },
            {
                "airline": "British Airways",
                "flight_number": "BA082",
                "departure": payload.origin,
                "arrival": payload.destination,
                "price": "670",
                "currency": "USD",
                "duration": "7h 30m",
                "stops": "Direct",
                "baggage": "23kg"
            },
            {
                "airline": "Lufthansa",
                "flight_number": "LH556",
                "departure": payload.origin,
                "arrival": payload.destination,
                "price": "590",
                "currency": "USD",
                "duration": "8h 15m",
                "stops": "1 Stop",
                "baggage": "23kg"
            },
            {
                "airline": "EgyptAir",
                "flight_number": "MS878",
                "departure": payload.origin,
                "arrival": payload.destination,
                "price": "370",
                "currency": "USD",
                "duration": "5h 50m",
                "stops": "Direct",
                "baggage": "25kg"
            },
            {
                "airline": "Air France",
                "flight_number": "AF241",
                "departure": payload.origin,
                "arrival": payload.destination,
                "price": "640",
                "currency": "USD",
                "duration": "8h 05m",
                "stops": "1 Stop",
                "baggage": "23kg"
            },
            {
                "airline": "KLM Royal Dutch",
                "flight_number": "KL588",
                "departure": payload.origin,
                "arrival": payload.destination,
                "price": "610",
                "currency": "USD",
                "duration": "7h 45m",
                "stops": "1 Stop",
                "baggage": "23kg"
            },
            {
                "airline": "Royal Air Maroc",
                "flight_number": "AT221",
                "departure": payload.origin,
                "arrival": payload.destination,
                "price": "345",
                "currency": "USD",
                "duration": "6h 20m",
                "stops": "Direct",
                "baggage": "23kg"
            },
            {
                "airline": "Air Peace",
                "flight_number": "P4711",
                "departure": payload.origin,
                "arrival": payload.destination,
                "price": "280",
                "currency": "USD",
                "duration": "4h 55m",
                "stops": "Direct",
                "baggage": "20kg"
            }
        ]
    }