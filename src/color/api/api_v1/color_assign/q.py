from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from src.color.composition import ColorComposition
from src.core.api.responses import api_response
from src.core.db.database import get_db

color_assign_q_router = APIRouter(
    tags=["Назначения цветов"],
)


class ColorAssignResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    key: str
    color: str



@color_assign_q_router.get(
    path='/',
    response_model=list[ColorAssignResponse],
)
async def list_color_assigns(
    color: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Получить список всех назначений цветов."""
    queries = ColorComposition.build_color_assign_queries(db)
    results = await queries.list_color_assigns(color=color)
    return api_response([
        ColorAssignResponse(id=r.id, key=r.key, color=r.color)
        for r in results
    ])


@color_assign_q_router.get(
    path='/{assign_id}',
    response_model=ColorAssignResponse,
)
async def get_color_assign(
    assign_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Получить назначение по ID."""
    queries = ColorComposition.build_color_assign_queries(db)
    result = await queries.get_color_assign(assign_id)
    return api_response(ColorAssignResponse(
        id=result.id,
        key=result.key,
        color=result.color,
    ))
