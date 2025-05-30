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
    PG_SCHEMA2: str
    
    api_key: str

    cors_origins1:str
    cors_origins2:str


    CARPETA_ORIGEN_MUTACIONES: str
    CARPETA_EXITOSO_MUTACIONES: str
    CARPETA_FALLIDO_MUTACIONES: str

    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USER: str
    SMTP_PASS: str
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
