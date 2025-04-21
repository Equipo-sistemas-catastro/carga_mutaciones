
from fastapi_pagination import Params as BaseParams


from typing import Generic, List, TypeVar
from pydantic import BaseModel
from fastapi_pagination.bases import AbstractPage, RawParams

T = TypeVar("T")

class CustomParams(BaseParams):
    def __init__(self, page: int = 1, size: int = 10):
        super().__init__(page=page, size=size)

class CustomPage(BaseModel, Generic[T]):
    total: int
    page: int
    size: int
    pages: int
    items: List[T]

    __params_type__ = RawParams

    @classmethod
    def create(cls, items: List[T], total: int, params: RawParams) -> "CustomPage":
        pages = (total + params.size - 1) // params.size
        return cls(
            total=total,
            page=params.page,
            size=params.size,
            pages=pages,
            items=items
        )
