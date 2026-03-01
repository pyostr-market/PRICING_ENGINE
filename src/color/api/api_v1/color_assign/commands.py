from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.color.api.api_v1.color_assign.schemas import (
    ColorAssignCreateRequest,
    ColorAssignResponse,
    ColorAssignUpdateRequest,
)
from src.color.application.dto.color import ColorAssignCreateDTO, ColorAssignUpdateDTO
from src.color.composition import ColorComposition
from src.core.api.responses import api_response
from src.core.auth.dependencies import get_current_user, require_permissions
from src.core.auth.schemas.user import User
from src.core.db.database import get_db

color_assign_commands_router = APIRouter(
    tags=["Назначения цветов"],
)


@color_assign_commands_router.post(
    path='/',
    response_model=ColorAssignResponse,
    dependencies=[Depends(require_permissions("pricing_engine:create"))],

)
async def create_color_assign(
    request: ColorAssignCreateRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Создать новое назначение цвета."""
    dto = ColorAssignCreateDTO(key=request.key, color=request.color)
    command = ColorComposition.build_create_color_assign_command(db)
    result = await command.execute(dto, user)
    return api_response(ColorAssignResponse(
        id=result.id,
        key=result.key,
        color=result.color,
    ))


@color_assign_commands_router.put(
    path='/{assign_id}',
    response_model=ColorAssignResponse,
    dependencies=[Depends(require_permissions("pricing_engine:update"))],
)
async def update_color_assign(
    assign_id: int,
    request: ColorAssignUpdateRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Обновить существующее назначение."""
    dto = ColorAssignUpdateDTO(key=request.key, color=request.color)
    command = ColorComposition.build_update_color_assign_command(db)
    result = await command.execute(assign_id, dto, user)
    return api_response(ColorAssignResponse(
        id=result.id,
        key=result.key,
        color=result.color,
    ))


@color_assign_commands_router.delete(
    path='/{assign_id}',
    dependencies=[Depends(require_permissions("pricing_engine:delete"))],
)
async def delete_color_assign(
    assign_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Удалить назначение."""
    command = ColorComposition.build_delete_color_assign_command(db)
    result = await command.execute(assign_id, user)
    return api_response({"deleted": result})
