from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class PriceCreateRequest(BaseModel):
    """Запрос на создание прайса"""
    category: str = Field(..., description="Название категории", min_length=1, max_length=100)
    supplier: str = Field(..., description="Название поставщика", min_length=1, max_length=200)
    region: str = Field(..., description="Название региона", min_length=1, max_length=100)
    price_text: str = Field(..., description="Текст прайса", min_length=1)


class PriceUpdateRequest(BaseModel):
    """Запрос на обновление прайса"""
    category: Optional[str] = Field(None, description="Название категории", min_length=1, max_length=100)
    supplier: Optional[str] = Field(None, description="Название поставщика", min_length=1, max_length=200)
    region: Optional[str] = Field(None, description="Название региона", min_length=1, max_length=100)
    price_text: Optional[str] = Field(None, description="Текст прайса", min_length=1)


class PriceResponse(BaseModel):
    """Ответ с данными прайса"""
    model_config = ConfigDict(from_attributes=True)
    id: int
    category: str
    supplier: str
    region: str
    price_text: str
