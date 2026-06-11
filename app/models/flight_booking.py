# app/models/flight_booking.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
)
from sqlalchemy.sql import func

from app.db.base_class import Base


class FlightBooking(Base):
    __tablename__ = "flight_bookings"

    id = Column(Integer, primary_key=True, index=True)

    booking_reference = Column(
        String,
        unique=True
    )

    airline = Column(String)

    origin = Column(String)
    destination = Column(String)

    departure_date = Column(String)
    return_date = Column(
        String,
        nullable=True
    )

    # Passenger Information
    first_name = Column(String)
    middle_name = Column(String, nullable=True)
    last_name = Column(String)

    gender = Column(String)
    date_of_birth = Column(String)

    nationality = Column(String)

    # Passport Information
    passport_number = Column(String)

    passport_issue_date = Column(
        String
    )

    passport_expiry_date = Column(
        String
    )

    passport_issuing_country = Column(
        String
    )

    # Contact Information
    email = Column(String)
    phone = Column(String)

    # Travel
    travel_class = Column(String)

    amount = Column(Float)

    payment_status = Column(
        String,
        default="pending"
    )

    booking_status = Column(
        String,
        default="pending"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    payment_reference = Column(
    String,
    nullable=True
)

payment_status = Column(
    String,
    default="pending"
)

booking_status = Column(
    String,
    default="pending"
)