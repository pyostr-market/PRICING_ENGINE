from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.color.api.api_v1.color.schemas import (
    ColorCreateRequest,
    ColorResponse,
    ColorUpdateRequest,
)
from src.color.application.dto.color import ColorDTO
from src.color.composition import ColorComposition
from src.core.api.responses import api_response
from src.core.auth.dependencies import get_current_user, require_permissions
from src.core.auth.schemas.user import User
from src.core.db.database import get_db

color_commands_router = APIRouter(
    tags=["Цвета"],
)


@color_commands_router.post(
    path='/',
    response_model=ColorResponse,
    dependencies=[Depends(require_permissions("pricing_engine:create"))],

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
    dependencies=[Depends(require_permissions("pricing_engine:update"))],

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
    dependencies=[Depends(require_permissions("pricing_engine:delete"))],

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
