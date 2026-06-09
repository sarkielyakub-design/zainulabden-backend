from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    packages,
    bookings,
    admin,
    ticketst,
    contact,
)

# =====================================
# MAIN API ROUTER
# =====================================
api_router = APIRouter()

# =====================================
# AUTH ROUTES
# =====================================
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"],
)

# =====================================
# USER ROUTES
# =====================================
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)

# =====================================
# PACKAGE ROUTES
# =====================================
api_router.include_router(
    packages.router,
    prefix="/packages",
    tags=["Packages"],
)

# =====================================
# BOOKING ROUTES
# =====================================
api_router.include_router(
    bookings.router,
    prefix="/bookings",
    tags=["Bookings"],
)

# =====================================
# ADMIN ROUTES
# =====================================
api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["Admin"],
)

# =====================================
# TICKET ROUTES
# =====================================
api_router.include_router(
    ticketst.router,
    prefix="/tickets",
    tags=["Tickets"],
)

# =====================================
# CONTACT ROUTES
# =====================================
api_router.include_router(
    contact.router,
    prefix="/contact",
    tags=["Contact"],
)