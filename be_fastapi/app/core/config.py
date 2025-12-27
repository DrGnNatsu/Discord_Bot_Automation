import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    HASH_ALGORITHM: str = os.getenv("HASH_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_HOUR: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOUR"))
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN")
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()