from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth.dependencies import require_permissions
from src.color.api.api_v1.color.schemas import ColorResponse
from src.color.composition import ColorComposition
from src.core.api.responses import api_response
from src.core.api.schemas import PaginatedDataSchema
from src.core.auth.schemas.user import User
from src.core.db.database import get_db

color_q_router = APIRouter(
    tags=["Цвета"],
)


@color_q_router.get(
    path='/',
    response_model=PaginatedDataSchema[ColorResponse],
    dependencies=[Depends(require_permissions("pricing_engine:view"))],

)
async def list_colors(
    limit: Annotated[int, Query(ge=1, le=1000)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    db: AsyncSession = Depends(get_db),
):
    """Получить список всех цветов."""
    queries = ColorComposition.build_color_queries(db)
    results, total = await queries.list_colors(limit=limit, offset=offset)
    return api_response(PaginatedDataSchema(
        items=[ColorResponse(name=r.name) for r in results],
        total=total,
    ))


@color_q_router.get(
    path='/{name}',
    response_model=ColorResponse,
    dependencies=[Depends(require_permissions("pricing_engine:view"))],
)
async def get_color(
    name: str,
    db: AsyncSession = Depends(get_db),
):
    """Получить цвет"""
    queries = ColorComposition.build_color_queries(db)
    result = await queries.get_color(name)
    return api_response(ColorResponse(name=result.name))
