from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):

    # =========================
    # PROJECT
    # =========================
    PROJECT_NAME: str

    # =========================
    # DATABASE
    # =========================
    DATABASE_URL: str

    # =========================
    # JWT
    # =========================
    SECRET_KEY: str

    ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # =========================
    # PAYSTACK
    # =========================
    PAYSTACK_SECRET_KEY: str

    PAYSTACK_PUBLIC_KEY: str
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()