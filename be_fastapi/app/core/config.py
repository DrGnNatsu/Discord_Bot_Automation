import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DATABASE_URL_APP: str = os.getenv("DATABASE_URL_APP")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    HASH_ALGORITHM: str = os.getenv("HASH_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_HOUR: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOUR"))
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"


settings = Settings()