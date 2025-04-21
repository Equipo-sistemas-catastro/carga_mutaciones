# backend/app/core/config.py

from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_DB: str
    PG_PORT: int
    PG_SCHEMA: str

    CARPETA_ORIGEN_MUTACIONES: str
    CARPETA_EXITOSO_MUTACIONES: str
    CARPETA_FALLIDO_MUTACIONES: str

settings = Settings()
