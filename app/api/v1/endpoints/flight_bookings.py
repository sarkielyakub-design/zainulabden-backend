from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from app.db.session import get_db
from app.models.flight_booking import FlightBooking
from app.schemas.flight_booking import FlightBookingCreate

router = APIRouter(
    prefix="/flight-bookings",
    tags=["Flight Bookings"]
)


@router.post("/")
async def create_booking(
    payload: FlightBookingCreate,
    db: Session = Depends(get_db)
):

    reference = f"FLT-{str(uuid4())[:8]}"

    booking = FlightBooking(
        booking_reference=reference,

        airline=payload.airline,

        origin=payload.origin,
        destination=payload.destination,

        departure_date=payload.departure_date,
        return_date=payload.return_date,

        first_name=payload.first_name,
        middle_name=payload.middle_name,
        last_name=payload.last_name,

        gender=payload.gender,
        date_of_birth=payload.date_of_birth,

        nationality=payload.nationality,

        passport_number=payload.passport_number,
        passport_issue_date=payload.passport_issue_date,
        passport_expiry_date=payload.passport_expiry_date,
        passport_issuing_country=payload.passport_issuing_country,

        email=payload.email,
        phone=payload.phone,

        travel_class=payload.travel_class,

        amount=payload.amount,

        payment_status="pending",
        booking_status="pending"
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return {
        "booking_reference": reference,
        "booking_id": booking.id,
        "payment_status": booking.payment_status,
        "booking_status": booking.booking_status,
        "message": "Booking created successfully"
    }
@router.get("/")
async def get_bookings(
    db: Session = Depends(get_db)
):
    bookings = db.query(
        FlightBooking
    ).all()

    return bookings
@router.get("/{booking_id}")
async def get_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    booking = (
        db.query(FlightBooking)
        .filter(
            FlightBooking.id == booking_id
        )
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return booking
@router.put("/{booking_id}/confirm")
async def confirm_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    booking = (
        db.query(FlightBooking)
        .filter(
            FlightBooking.id == booking_id
        )
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    booking.booking_status = "confirmed"

    db.commit()

    return {
        "message": "Booking confirmed"
    }
@router.put("/{booking_id}/ticketed")
async def ticket_issued(
    booking_id: int,
    db: Session = Depends(get_db)
):
    booking = (
        db.query(FlightBooking)
        .filter(
            FlightBooking.id == booking_id
        )
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    booking.booking_status = "ticketed"

    db.commit()

    return {
        "message": "Ticket issued"
    }