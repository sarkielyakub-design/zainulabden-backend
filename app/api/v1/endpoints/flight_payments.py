from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests

from app.db.session import get_db
from app.models.flight_booking import FlightBooking
from app.schemas.flight_payment import FlightPaymentRequest
from app.core.config import settings

router = APIRouter(
    prefix="/flight-payments",
    tags=["Flight Payments"]
)


@router.post("/initialize")
async def initialize_payment(
    payload: FlightPaymentRequest,
    db: Session = Depends(get_db)
):

    booking = (
        db.query(FlightBooking)
        .filter(
            FlightBooking.id == payload.booking_id
        )
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    headers = {
        "Authorization":
        f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type":
        "application/json"
    }

    data = {
        "email": booking.email,
        "amount": int(
            booking.amount * 100
        )
    }

    response = requests.post(
        "https://api.paystack.co/transaction/initialize",
        headers=headers,
        json=data
    )

    result = response.json()

    if not result.get("status"):
        raise HTTPException(
            status_code=400,
            detail="Payment initialization failed"
        )

    booking.payment_reference = (
        result["data"]["reference"]
    )

    booking.payment_url = (
        result["data"]["authorization_url"]
    )

    db.commit()

    return {
        "payment_url":
        booking.payment_url
    }
@router.get("/verify/{reference}")
async def verify_payment(
    reference: str,
    db: Session = Depends(get_db)
):
    booking = (
        db.query(FlightBooking)
        .filter(
            FlightBooking.payment_reference == reference
        )
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    headers = {
        "Authorization":
        f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }

    response = requests.get(
        f"https://api.paystack.co/transaction/verify/{reference}",
        headers=headers
    )

    result = response.json()

    if not result.get("status"):
        raise HTTPException(
            status_code=400,
            detail="Payment verification failed"
        )

    if result["data"]["status"] == "success":
        booking.payment_status = "paid"
        booking.booking_status = "confirmed"

    else:
        booking.payment_status = "failed"
        booking.booking_status = "cancelled"

    db.commit()

    return {
        "payment_status": booking.payment_status,
        "booking_status": booking.booking_status,
        "message": "Payment verification completed"
    }