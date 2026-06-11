from amadeus import Client, ResponseError
from app.core.config import settings

amadeus = Client(
    client_id=settings.AMADEUS_API_KEY,
    client_secret=settings.AMADEUS_API_SECRET
)

def search_flights(
    origin,
    destination,
    departure_date,
    adults
):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=departure_date,
            adults=adults,
            max=20
        )

        return response.data

    except ResponseError as error:
        return {"error": str(error)}