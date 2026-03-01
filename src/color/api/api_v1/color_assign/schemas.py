from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ColorAssignCreateRequest(BaseModel):
    key: str = Field(..., description="Ключ назначения", min_length=1, max_length=50)
    color: str = Field(..., description="Название цвета", min_length=1, max_length=50)


class ColorAssignUpdateRequest(BaseModel):
    key: Optional[str] = Field(None, description="Ключ назначения", min_length=1, max_length=50)
    color: Optional[str] = Field(None, description="Название цвета", min_length=1, max_length=50)


class ColorAssignResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    key: str
    color: str

