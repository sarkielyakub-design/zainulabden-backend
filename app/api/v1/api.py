from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    packages,
    bookings,
    admin,
    ticketst,
    contact,
    flights,
    flight_bookings,
    flight_payments,
)

api_router = APIRouter()

# Auth
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"],
)

# Users
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)

# Packages
api_router.include_router(
    packages.router,
    prefix="/packages",
    tags=["Packages"],
)

# Bookings
api_router.include_router(
    bookings.router,
    prefix="/bookings",
    tags=["Bookings"],
)

# Admin
api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["Admin"],
)

# Tickets
api_router.include_router(
    ticketst.router,
    prefix="/tickets",
    tags=["Tickets"],
)

# Contact
api_router.include_router(
    contact.router,
    prefix="/contact",
    tags=["Contact"],
)

# Flights
api_router.include_router(
    flights.router
)

# Flight Bookings
api_router.include_router(
    flight_bookings.router,
    prefix="/flight-bookings",
    tags=["Flight Bookings"],
)

# Flight Payments
api_router.include_router(
    flight_payments.router,
    prefix="/flight-payments",
    tags=["Flight Payments"],
)