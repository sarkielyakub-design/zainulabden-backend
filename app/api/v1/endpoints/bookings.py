from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Body,
    Request,
)

from sqlalchemy.orm import Session

from datetime import (
    datetime,
    timedelta,
)

import requests
import uuid
import hmac
import hashlib
import json
import os
import logging

from app.api.deps import (
    get_current_user,
    get_db,
)

from app.models.bookings import Booking
from app.models.package import Package
from app.models.ticket import Ticket

from app.schemas.bookings import (
    BookingCreate,
)

from app.core.config import settings

from app.services.email import (
    send_booking_email,
)

from app.services.payment_service import (
    process_successful_payment,
)

router = APIRouter(tags=["Bookings"])

logger = logging.getLogger(__name__)

PAYSTACK_URL = (
    "https://api.paystack.co/transaction/initialize"
)


# =========================================================
# CREATE PACKAGE BOOKING + PAYMENT
# =========================================================
@router.post(
    "/create-and-pay",
    status_code=201
)
def create_and_pay(
    package_id: int,

    data: BookingCreate =
    Body(...),

    db: Session =
    Depends(get_db),

    user =
    Depends(get_current_user),
):

    try:

        # =========================================================
        # FIND PACKAGE
        # =========================================================
        package = (
            db.query(Package)
            .filter(
                Package.id == package_id
            )
            .first()
        )

        if not package:
            raise HTTPException(
                404,
                "Package not found"
            )

        # =========================================================
        # SLOT CHECK
        # =========================================================
        if (
            package.booked_slots >=
            package.total_slots
        ):
            raise HTTPException(
                400,
                "No available slots"
            )

        # =========================================================
        # DUPLICATE CHECK
        # =========================================================
        existing = (
            db.query(Booking)
            .filter(
                Booking.user_id == user.id,
                Booking.package_id == package.id,
                Booking.status == "pending",
            )
            .first()
        )

        if existing:

            if (
                existing.expires_at and
                existing.expires_at <
                datetime.utcnow()
            ):

                existing.status = (
                    "cancelled"
                )

                db.commit()

            else:

                return {
                    "message":
                        "Pending booking already exists",

                    "booking_id":
                        existing.id,

                    "authorization_url":
                        existing.payment_url,

                    "reference":
                        existing.payment_reference,
                }

        # =========================================================
        # REFERENCE
        # =========================================================
        reference = (
            f"BOOK-{uuid.uuid4().hex}"
        )

        # =========================================================
        # DATE VALIDATION
        # =========================================================
        try:

            dob = datetime.strptime(
                data.date_of_birth,
                "%Y-%m-%d"
            ).date()

            issue = datetime.strptime(
                data.passport_issue,
                "%Y-%m-%d"
            ).date()

            expiry = datetime.strptime(
                data.passport_expiry,
                "%Y-%m-%d"
            ).date()

        except:
            raise HTTPException(
                400,
                "Invalid date format"
            )

        # =========================================================
        # PRICE
        # =========================================================
        amount_kobo = int(
            package.price * 100
        )

        # =========================================================
        # CREATE BOOKING
        # =========================================================
        booking = Booking(

            user_id=user.id,

            package_id=package.id,

            surname=data.surname,

            first_name=data.first_name,

            given_names=data.given_names,

            nationality=data.nationality,

            email=data.email,

            phone=data.phone,

            passport_number=data.passport_number,

            place_of_birth=data.place_of_birth,

            date_of_birth=dob,

            passport_issue=issue,

            passport_expiry=expiry,

            amount=package.price,

            status="pending",

            payment_reference=reference,

            expires_at=(
                datetime.utcnow()
                + timedelta(minutes=15)
            ),
        )

        db.add(booking)
        db.commit()
        db.refresh(booking)

        # =========================================================
        # PAYSTACK
        # =========================================================
        payload = {
            "email": booking.email,

            "amount": amount_kobo,

            "reference": reference,

            "callback_url":
                f"{os.getenv('FRONTEND_URL')}/payment-success",
        }

        headers = {
            "Authorization":
                f"Bearer {settings.PAYSTACK_SECRET_KEY}",

            "Content-Type":
                "application/json",
        }

        response = requests.post(
            PAYSTACK_URL,
            json=payload,
            headers=headers,
            timeout=30,
        )

        response = response.json()

        if not response.get("status"):

            db.delete(booking)
            db.commit()

            raise HTTPException(
                400,
                response.get("message")
            )

        booking.payment_url = (
            response["data"][
                "authorization_url"
            ]
        )

        db.commit()

        return {
            "booking_id":
                booking.id,

            "authorization_url":
                booking.payment_url,

            "reference":
                reference,
        }

    except requests.exceptions.Timeout:

        db.rollback()

        raise HTTPException(
            504,
            "Payment gateway timeout"
        )

    except Exception as e:

        db.rollback()

        logger.error(
            f"PACKAGE CREATE ERROR: {e}"
        )

        raise HTTPException(
            500,
            str(e)
        )


# =========================================================
# CREATE TICKET BOOKING + PAYMENT
# =========================================================
@router.post(
    "/create-and-pay-ticket",
    status_code=201
)
def create_and_pay_ticket(
    ticket_id: int,

    data: BookingCreate =
    Body(...),

    db: Session =
    Depends(get_db),

    user =
    Depends(get_current_user),
):

    try:

        # =========================================================
        # FIND TICKET
        # =========================================================
        ticket = (
            db.query(Ticket)
            .filter(
                Ticket.id == ticket_id
            )
            .first()
        )

        if not ticket:
            raise HTTPException(
                404,
                "Ticket not found"
            )

        # =========================================================
        # REFERENCE
        # =========================================================
        reference = (
            f"TICKET-{uuid.uuid4().hex}"
        )

        # =========================================================
        # DATES
        # =========================================================
        try:

            dob = datetime.strptime(
                data.date_of_birth,
                "%Y-%m-%d"
            ).date()

            issue = datetime.strptime(
                data.passport_issue,
                "%Y-%m-%d"
            ).date()

            expiry = datetime.strptime(
                data.passport_expiry,
                "%Y-%m-%d"
            ).date()

        except:
            raise HTTPException(
                400,
                "Invalid date format"
            )

        # =========================================================
        # PRICE
        # =========================================================
        amount_kobo = int(
            ticket.price * 100
        )

        # =========================================================
        # CREATE BOOKING
        # =========================================================
        booking = Booking(

            user_id=user.id,

            ticket_id=ticket.id,

            surname=data.surname,

            first_name=data.first_name,

            given_names=data.given_names,

            nationality=data.nationality,

            email=data.email,

            phone=data.phone,

            passport_number=data.passport_number,

            place_of_birth=data.place_of_birth,

            date_of_birth=dob,

            passport_issue=issue,

            passport_expiry=expiry,

            amount=ticket.price,

            status="pending",

            payment_reference=reference,

            expires_at=(
                datetime.utcnow()
                + timedelta(minutes=15)
            ),
        )

        db.add(booking)
        db.commit()
        db.refresh(booking)

        # =========================================================
        # PAYSTACK
        # =========================================================
        payload = {
            "email": booking.email,

            "amount": amount_kobo,

            "reference": reference,

            "callback_url":
                f"{os.getenv('FRONTEND_URL')}/payment-success",
        }

        headers = {
            "Authorization":
                f"Bearer {settings.PAYSTACK_SECRET_KEY}",

            "Content-Type":
                "application/json",
        }

        response = requests.post(
            PAYSTACK_URL,
            json=payload,
            headers=headers,
            timeout=30,
        )

        response = response.json()

        if not response.get("status"):

            db.delete(booking)
            db.commit()

            raise HTTPException(
                400,
                response.get("message")
            )

        booking.payment_url = (
            response["data"][
                "authorization_url"
            ]
        )

        db.commit()

        return {
            "booking_id":
                booking.id,

            "authorization_url":
                booking.payment_url,

            "reference":
                reference,
        }

    except requests.exceptions.Timeout:

        db.rollback()

        raise HTTPException(
            504,
            "Payment gateway timeout"
        )

    except Exception as e:

        db.rollback()

        logger.error(
            f"TICKET CREATE ERROR: {e}"
        )

        raise HTTPException(
            500,
            str(e)
        )


# =========================================================
# VERIFY PAYMENT
# =========================================================
@router.get("/verify/{reference}")
def verify_payment(
    reference: str,
    db: Session = Depends(get_db),
):

    url = (
        f"https://api.paystack.co/transaction/verify/{reference}"
    )

    headers = {
        "Authorization":
            f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }

    res = requests.get(
        url,
        headers=headers
    ).json()

    if not res.get("status"):
        raise HTTPException(
            400,
            "Verification failed"
        )

    data = res["data"]

    booking = (
        db.query(Booking)
        .filter(
            Booking.payment_reference == reference
        )
        .first()
    )

    if not booking:
        raise HTTPException(
            404,
            "Booking not found"
        )

    if (
        booking.expires_at and
        booking.expires_at <
        datetime.utcnow()
    ):

        booking.status = (
            "cancelled"
        )

        db.commit()

        raise HTTPException(
            400,
            "Booking expired"
        )

    if booking.status == "paid":
        return {"success": True}

    if data["status"] != "success":
        raise HTTPException(
            400,
            "Payment failed"
        )

    # SUCCESS
    process_successful_payment(
        booking,
        db
    )

    return {
        "success": True
    }