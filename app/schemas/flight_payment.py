# app/schemas/flight_payment.py

from pydantic import BaseModel


class FlightPaymentRequest(BaseModel):
    booking_id: int