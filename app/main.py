from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination
from fastapi.responses import FileResponse
from app.api.v1 import endpoints
from fastapi.security.api_key import APIKeyHeader
from fastapi.openapi.models import APIKey, APIKeyIn, SecuritySchemeType
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.security import validar_api_key
import os

#app = FastAPI()

# 👇 Configuración de FastAPI
app = FastAPI(
    title="API Mutaciones",
    version="1.0.0",
    dependencies=[Depends(validar_api_key)]
)

cors_origins1=settings.cors_origins1
cors_origins2=settings.cors_origins2


# 👇 Configuración de CORS
#origins = [origin.strip() for origin in cors_origins.split(",") if origin.strip()]
origins = [
    cors_origins1,cors_origins2
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # puedes usar ["*"] para permitir todos (solo en desarrollo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(endpoints.router, prefix="/api/v1")
add_pagination(app)

#Para llamar el ícono de los endpoints
@app.get("/favicon.ico")
async def favicon():
    file_path = os.path.join(os.path.dirname(__file__), "static", "favicon.ico")
    return FileResponse(file_path)


# Personaliza el esquema de seguridad para llamar las API
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="API Mutaciones",
        version="1.0.0",
        description="API protegida con API Key en header",
        routes=app.routes,
    )

    # 👇 Asegura que 'components' existe antes de usarla
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    openapi_schema["components"]["securitySchemes"] = {
        "APIKeyHeader": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key"
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"APIKeyHeader": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

