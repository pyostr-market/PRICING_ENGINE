from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth.dependencies import require_permissions
from src.color.composition import ColorComposition
from src.core.api.responses import api_response
from src.core.api.schemas import PaginatedDataSchema
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
    response_model=PaginatedDataSchema[ColorAssignResponse],
    dependencies=[Depends(require_permissions("pricing_engine:view"))],

)
async def list_color_assigns(
    color: Optional[str] = None,
    limit: Annotated[int, Query(ge=1, le=1000)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    db: AsyncSession = Depends(get_db),
):
    """Получить список всех назначений цветов."""
    queries = ColorComposition.build_color_assign_queries(db)
    results, total = await queries.list_color_assigns(color=color, limit=limit, offset=offset)
    return api_response(PaginatedDataSchema(
        items=[
            ColorAssignResponse(id=r.id, key=r.key, color=r.color)
            for r in results
        ],
        total=total,
    ))


@color_assign_q_router.get(
    path='/{assign_id}',
    response_model=ColorAssignResponse,
    dependencies=[Depends(require_permissions("pricing_engine:view"))],
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
