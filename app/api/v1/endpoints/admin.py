from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import os
import uuid
from app.models.contact import ContactMessage
from app.models.bookings import Booking  # make sure exists
from app.api.deps import get_db, require_admin
from app.models.package import Package
from app.services.payment_service import process_successful_payment
import cloudinary.uploader
from app.utils.cloudinary import cloudinary  # make sure this exists
from app.models.package import Package
from app.models.ticket import Ticket
from app.models.bookings import Booking
from app.models.package import Package
from app.models.user import User
router = APIRouter()

UPLOAD_DIR = "uploads"


# =========================
# 👑 CREATE PACKAGE
# =========================
@router.post("/packages")
async def create_package(
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),

    flight_name: Optional[str] = Form(""),
    flight_from: Optional[str] = Form(""),
    flight_to: Optional[str] = Form(""),

    departure_date: Optional[str] = Form(""),
    return_date: Optional[str] = Form(""),

    hotel_name: Optional[str] = Form(""),
    hotel_rating: Optional[str] = Form("3"),

    category: Optional[str] = Form("standard"),

    duration_days: int = Form(0),
    total_slots: int = Form(0),
    booked_slots: int = Form(0),

    file: UploadFile = File(None),

    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    image_url = None

    # 📸 CLOUDINARY UPLOAD (FIXED)
    if file:
        try:
            result = cloudinary.uploader.upload(
                file.file,
                folder="packages",  # optional (good practice)
                resource_type="image"
            )

            image_url = result.get("secure_url")

        except Exception as e:
            raise HTTPException(500, f"Image upload failed: {str(e)}")

    # 🧱 CREATE PACKAGE
    new_package = Package(
        title=title,
        description=description,
        price=price,

        flight_name=flight_name,
        flight_from=flight_from,
        flight_to=flight_to,

        departure_date=departure_date,
        return_date=return_date,

        hotel_name=hotel_name,
        hotel_rating=hotel_rating,

        category=category,

        duration_days=duration_days,
        total_slots=total_slots,
        booked_slots=booked_slots,

        image_url=image_url
    )

    db.add(new_package)
    db.commit()
    db.refresh(new_package)

    return {
        "success": True,
        "message": "Package created",
        "data": new_package
    }

# =========================
# 👑 GET ALL (ADMIN)
# =========================
@router.get("/packages")
def get_admin_packages(
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    packages = db.query(Package).all()

    return {
        "success": True,
        "total": len(packages),
        "data": packages
    }


# =========================
# 👑 UPDATE PACKAGE
# =========================
@router.put("/packages/{package_id}")
async def update_package(
    package_id: int,

    title: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),

    flight_name: str = Form(""),
    flight_from: str = Form(""),
    flight_to: str = Form(""),

    departure_date: str = Form(""),
    return_date: str = Form(""),

    hotel_name: str = Form(""),
    hotel_rating: str = Form("3"),

    category: str = Form("standard"),

    duration_days: int = Form(0),
    total_slots: int = Form(0),

    file: UploadFile = File(None),  # 🔥 NEW

    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    package = db.query(Package).filter(Package.id == package_id).first()

    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    # ✏️ UPDATE BASIC FIELDS
    package.title = title
    package.description = description
    package.price = price

    package.flight_name = flight_name
    package.flight_from = flight_from
    package.flight_to = flight_to

    package.departure_date = departure_date
    package.return_date = return_date

    package.hotel_name = hotel_name
    package.hotel_rating = hotel_rating

    package.category = category

    package.duration_days = duration_days
    package.total_slots = total_slots

    # 📸 HANDLE IMAGE UPDATE
    if file:
        try:
            # 🔥 DELETE OLD IMAGE (VERY IMPORTANT)
            if package.public_id:
                cloudinary.uploader.destroy(package.public_id)

            # 🔥 UPLOAD NEW IMAGE
            result = cloudinary.uploader.upload(
                file.file,
                folder="packages",
                transformation=[
                    {"width": 800, "height": 600, "crop": "fill"},
                    {"quality": "auto"},
                    {"fetch_format": "auto"}
                ]
            )

            package.image_url = result.get("secure_url")
            package.public_id = result.get("public_id")

        except Exception as e:
            raise HTTPException(500, f"Image update failed: {str(e)}")

    db.commit()
    db.refresh(package)

    return {
        "success": True,
        "message": "Package updated",
        "data": package
    }
# =========================
# 👑 DELETE PACKAGE
# =========================
import cloudinary.uploader

@router.delete("/packages/{package_id}")
def delete_package(
    package_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    package = db.query(Package).filter(Package.id == package_id).first()

    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    # 🔥 DELETE IMAGE FROM CLOUDINARY
    try:
        if package.public_id:
            cloudinary.uploader.destroy(package.public_id)
    except Exception as e:
        print(f"Cloudinary delete failed: {e}")  # don't break deletion

    db.delete(package)
    db.commit()

    return {
        "success": True,
        "message": "Package deleted"
    }

# =========================
# 📸 UPLOAD IMAGE ONLY
# =========================
@router.post("/packages/{package_id}/upload")
async def upload_image(
    package_id: int,
    file: UploadFile = File(...),

    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    package = db.query(Package).filter(Package.id == package_id).first()

    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    package.image_url = f"/{UPLOAD_DIR}/{filename}"

    db.commit()
    db.refresh(package)

    return {
        "success": True,
        "image_url": package.image_url
    }
# =========================================================
# GET ALL BOOKINGS
# =========================================================
@router.get("/bookings")
def get_admin_bookings(
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):

    bookings = (
        db.query(Booking)
        .order_by(Booking.created_at.desc())
        .all()
    )

    results = []

    for booking in bookings:

        package_title = None
        ticket_airline = None
        from_airport = None
        to_airport = None

        # PACKAGE
        if booking.package_id:

            package = (
                db.query(Package)
                .filter(
                    Package.id == booking.package_id
                )
                .first()
            )

            if package:
                package_title = package.title

        # TICKET
        if booking.ticket_id:

            ticket = (
                db.query(Ticket)
                .filter(
                    Ticket.id == booking.ticket_id
                )
                .first()
            )

            if ticket:
                ticket_airline = ticket.airline
                from_airport = ticket.from_airport
                to_airport = ticket.to_airport

        results.append({

            "id": booking.id,

            "surname": booking.surname,

            "first_name": booking.first_name,

            "email": booking.email,

            "phone": booking.phone,

            "amount": booking.amount,

            "status": booking.status,

            "created_at": booking.created_at,

            "package_id": booking.package_id,

            "ticket_id": booking.ticket_id,

            "package_title": package_title,

            "ticket_airline": ticket_airline,

            "from_airport": from_airport,

            "to_airport": to_airport,
        })

    return {
        "success": True,
        "total": len(results),
        "data": results
    }




# =========================
# 📊 ADMIN ANALYTICS
# =========================
# =========================
# 💰 MARK BOOKING AS PAID
# =========================
@router.put("/bookings/{booking_id}/pay")
def mark_booking_paid(
    booking_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(404, "Booking not found")

    if booking.status == "paid":
        return {
            "success": True,
            "message": "Already marked as paid"
        }

    # ✅ USE CENTRAL LOGIC
    process_successful_payment(booking, db)

    return {
        "success": True,
        "message": "Booking marked as paid and slot updated"
    }
@router.get("/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
):

    total_packages = (
        db.query(Package).count()
    )

    total_tickets = (
        db.query(Ticket).count()
    )

    total_bookings = (
        db.query(Booking).count()
    )

    total_users = (
        db.query(User).count()
    )

    paid_bookings = (
        db.query(Booking)
        .filter(
            Booking.status == "paid"
        )
        .all()
    )

    revenue = sum([
        booking.amount or 0
        for booking in paid_bookings
    ])

    recent_bookings = (
        db.query(Booking)
        .order_by(
            Booking.created_at.desc()
        )
        .limit(5)
        .all()
    )

    return {
        "packages": total_packages,

        "tickets": total_tickets,

        "bookings": total_bookings,

        "users": total_users,

        "revenue": revenue,

        "recent_bookings":
            recent_bookings,
    }
@router.get("/activity")
def get_activity(
    db: Session = Depends(get_db),
):

    recent_bookings = (
        db.query(Booking)
        .order_by(
            Booking.created_at.desc()
        )
        .limit(10)
        .all()
    )

    activities = []

    for booking in recent_bookings:

        if booking.ticket_id:
            activity_type = "ticket"
        else:
            activity_type = "package"

        activities.append({
            "id": booking.id,

            "type": activity_type,

            "customer":
                f"{booking.surname} {booking.first_name}",

            "status": booking.status,

            "created_at":
                booking.created_at,
        })

    return {
        "activities": activities
    }
# =========================================================
# MARK BOOKING AS PAID
# =========================================================
@router.put("/bookings/{booking_id}/pay")
def mark_booking_paid(
    booking_id: int,
    db: Session = Depends(get_db),
):

    booking = (
        db.query(Booking)
        .filter(
            Booking.id == booking_id
        )
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    # ALREADY PAID
    if booking.status == "paid":
        return {
            "message":
                "Already marked paid"
        }

    # UPDATE STATUS
    booking.status = "paid"

    db.commit()

    # PACKAGE SLOT UPDATE
    if booking.package_id:

        package = (
            db.query(Package)
            .filter(
                Package.id ==
                booking.package_id
            )
            .first()
        )

        if package:
            package.booked_slots += 1
            db.commit()

    return {
        "message":
            "Booking marked as paid"

    }
# =====================================
# ADMIN CONTACT MESSAGES
# =====================================
@router.get("/messages")
def get_contact_messages(
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):

    messages = (
        db.query(ContactMessage)
        .order_by(
            ContactMessage.created_at.desc()
        )
        .all()
    )

    return {
        "success": True,
        "total": len(messages),
        "data": messages,
    }
@router.get("/users")
def get_users(
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):

    users = db.query(User).all()

    data = []

    for user in users:

        data.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "address": user.address,
            "nationality": user.nationality,
            "role": user.role,
            "created_at": user.created_at,
        })

    return {
        "success": True,
        "total": len(data),
        "data": data,
    }