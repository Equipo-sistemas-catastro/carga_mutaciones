# backend/app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_DB: str
    PG_PORT: str
    PG_SCHEMA: str
    
    api_key: str

    CARPETA_ORIGEN_MUTACIONES: str
    CARPETA_EXITOSO_MUTACIONES: str
    CARPETA_FALLIDO_MUTACIONES: str
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
