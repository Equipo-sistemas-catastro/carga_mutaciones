from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from app.core.config import settings

#Con este py se hace el manejo de token de seguridad para las API

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def validate_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.api_key:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="No autorizado: clave inválida"
        )
