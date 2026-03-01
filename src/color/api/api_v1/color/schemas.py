from pydantic import BaseModel, Field, ConfigDict


class ColorCreateRequest(BaseModel):
    name: str = Field(..., description="Название цвета", min_length=1, max_length=50)


class ColorUpdateRequest(BaseModel):
    name: str = Field(..., description="Новое название цвета", min_length=1, max_length=50)


class ColorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
