from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorSchema(BaseModel):
    code: str
    message: str
    details: dict


class ApiSuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T


class ApiErrorResponse(BaseModel):
    success: bool = False
    error: ErrorSchema


class PaginationParams(BaseModel):
    """Параметры пагинации для запросов."""
    limit: int = Field(default=100, ge=1, le=1000, description="Максимальное количество записей")
    offset: int = Field(default=0, ge=0, description="Смещение от начала списка")


class PaginatedDataSchema(BaseModel, Generic[T]):
    """Данные с пагинацией."""
    items: list[T]
    total: int


class PaginatedResponse(BaseModel, Generic[T]):
    """Ответ с пагинацией."""
    success: bool = True
    data: PaginatedDataSchema[T]