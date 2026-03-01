from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.color.application.dto.color import ColorAssignCreateDTO, ColorAssignUpdateDTO
from src.color.composition import ColorComposition
from src.core.api.responses import api_response
from src.core.auth.dependencies import get_current_user
from src.core.auth.schemas.user import User
from src.core.db.database import get_db

color_assign_commands_router = APIRouter(
    tags=["Назначения цветов"],
)


class ColorAssignCreateRequest(BaseModel):
    key: str = Field(..., description="Ключ назначения", min_length=1, max_length=50)
    color: str = Field(..., description="Название цвета", min_length=1, max_length=50)


class ColorAssignUpdateRequest(BaseModel):
    key: Optional[str] = Field(None, description="Ключ назначения", min_length=1, max_length=50)
    color: Optional[str] = Field(None, description="Название цвета", min_length=1, max_length=50)


class ColorAssignResponse(BaseModel):
    id: int
    key: str
    color: str

    class Config:
        from_attributes = True


@color_assign_commands_router.post(
    path='/',
    response_model=ColorAssignResponse,
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
