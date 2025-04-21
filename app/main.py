from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.api.v1 import endpoints

app = FastAPI()
app.include_router(endpoints.router, prefix="/api/v1")
add_pagination(app)
