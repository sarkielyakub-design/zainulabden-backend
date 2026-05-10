from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    packages,
    bookings,
    admin,
    ticketst,
)


api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

api_router.include_router(
    packages.router,
    prefix="/packages",
    tags=["Packages"]
)

api_router.include_router(
    bookings.router,
    prefix="/bookings",
    tags=["Bookings"]
)

api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["Admin"]
)

api_router.include_router(
    ticketst.router,
    prefix="/tickets",
    tags=["Tickets"]
)