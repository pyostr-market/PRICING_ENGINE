from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.color.application.dto.color import ColorDTO
from src.color.composition import ColorComposition
from src.core.api.responses import api_response
from src.core.auth.dependencies import get_current_user
from src.core.auth.schemas.user import User
from src.core.db.database import get_db

color_commands_router = APIRouter(
    tags=["Цвета"],
)


class ColorCreateRequest(BaseModel):
    name: str = Field(..., description="Название цвета", min_length=1, max_length=50)


class ColorUpdateRequest(BaseModel):
    name: str = Field(..., description="Новое название цвета", min_length=1, max_length=50)


class ColorResponse(BaseModel):
    name: str

    class Config:
        from_attributes = True


@color_commands_router.post(
    path='/',
    response_model=ColorResponse,
)
async def create_color(
    request: ColorCreateRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Создать цвет"""
    dto = ColorDTO(name=request.name)
    command = ColorComposition.build_create_color_command(db)
    result = await command.execute(dto, user)
    return api_response(ColorResponse(name=result.name))


@color_commands_router.put(
    path='/{name}',
    response_model=ColorResponse,
)
async def update_color(
    name: str,
    request: ColorUpdateRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Обновить существующий цвет."""
    dto = ColorDTO(name=request.name)
    command = ColorComposition.build_update_color_command(db)
    result = await command.execute(name, dto, user)
    return api_response(ColorResponse(name=result.name))


@color_commands_router.delete(
    path='/{name}',
)
async def delete_color(
    name: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Удалить цвет."""
    command = ColorComposition.build_delete_color_command(db)
    result = await command.execute(name, user)
    return api_response({"deleted": result})
