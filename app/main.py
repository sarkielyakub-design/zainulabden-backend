from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import logging
import os

from app.api.v1.api import api_router
from app.db.base import Base
from app.db.session import engine
from app.core.init_db import init_admin


# =========================
# 🧠 LOGGING
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# =========================
# 📁 UPLOADS
# =========================
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================
# 🚀 APP
# =========================
app = FastAPI(
    title="ZAINULABIDEEN TRAVEL API",
    version="2.0.0",
    description="Premium Travel Booking System",
    swagger_ui_parameters={
        "persistAuthorization": True
    },
)


# =========================
# 🌐 CORS
# =========================
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://zainulabden-travel.vercel.app",
    "https://*.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# =========================
# 📁 STATIC FILES
# =========================
app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_DIR),
    name="uploads"
)


# =========================
# 🔌 STARTUP
# =========================
@app.on_event("startup")
def startup():

    logger.info("🚀 Starting API")

    Base.metadata.create_all(bind=engine)

    logger.info("✅ Database Ready")

    init_admin()

    logger.info("✅ Admin Ready")


# =========================
# 🔗 ROUTES
# =========================
app.include_router(
    api_router,
    prefix="/api/v1"
)


# =========================
# 🏠 ROOT
# =========================
@app.get("/")
def root():
    return {
        "message": "🚀 ZAINULABIDEEN API Running",
        "status": "healthy",
        "version": "2.0.0"
    }


# =========================
# ❤️ HEALTH
# =========================
@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# =========================
# 🔐 SWAGGER JWT
# =========================
from fastapi.openapi.utils import get_openapi


def custom_openapi():

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="ZAINULABIDEEN TRAVEL API",
        version="2.0.0",
        description="Premium Travel Booking System",
        routes=app.routes,
    )

    # KEEP EXISTING COMPONENTS
    components = openapi_schema.get(
        "components", {}
    )

    security_schemes = components.get(
        "securitySchemes", {}
    )

    # ADD JWT SECURITY
    security_schemes["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    components["securitySchemes"] = (
        security_schemes
    )

    openapi_schema["components"] = (
        components
    )

    openapi_schema["security"] = [
        {"BearerAuth": []}
    ]

    app.openapi_schema = (
        openapi_schema
    )

    return app.openapi_schema


app.openapi = custom_openapi