from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.color.composition import ColorComposition
from src.core.api.responses import api_response
from src.core.auth.schemas.user import User
from src.core.db.database import get_db

color_q_router = APIRouter(
    tags=["Цвета"],
)


class ColorResponse(BaseModel):
    name: str

    class Config:
        from_attributes = True


@color_q_router.get(
    path='/',
    response_model=list[ColorResponse],
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
)
async def get_color(
    name: str,
    db: AsyncSession = Depends(get_db),
):
    """Получить цвет"""
    queries = ColorComposition.build_color_queries(db)
    result = await queries.get_color(name)
    return api_response(ColorResponse(name=result.name))
