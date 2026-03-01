from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth.dependencies import require_permissions
from src.color.api.api_v1.color.schemas import ColorResponse
from src.color.composition import ColorComposition
from src.core.api.responses import api_response
from src.core.auth.schemas.user import User
from src.core.db.database import get_db

color_q_router = APIRouter(
    tags=["Цвета"],
)


@color_q_router.get(
    path='/',
    response_model=list[ColorResponse],
    dependencies=[Depends(require_permissions("pricing_engine:view"))],

)
async def list_colors(
    db: AsyncSession = Depends(get_db),
):
    """Получить список всех цветов."""
    queries = ColorComposition.build_color_queries(db)
    results = await queries.list_colors()
    return api_response([ColorResponse(name=r.name) for r in results])


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
