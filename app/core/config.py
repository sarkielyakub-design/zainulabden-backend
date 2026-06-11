from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str

    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    PAYSTACK_SECRET_KEY: str
    PAYSTACK_PUBLIC_KEY: str

    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str

    # AMADEUS
    AMADEUS_API_KEY: str = ""
    AMADEUS_API_SECRET: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()