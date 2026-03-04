from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.price.api.api_v1.price.schemas import PriceResponse
from src.price.composition import PriceComposition
from src.core.api.responses import api_response
from src.core.api.schemas import PaginatedDataSchema
from src.core.auth.dependencies import require_permissions
from src.core.db.database import get_db

price_q_router = APIRouter(
    tags=["Прайсы"],
)


@price_q_router.get(
    path='/',
    response_model=PaginatedDataSchema[PriceResponse],
    dependencies=[Depends(require_permissions("pricing_engine:view"))],
)
async def list_prices(
    category: Optional[str] = None,
    supplier: Optional[str] = None,
    region: Optional[str] = None,
    limit: Annotated[int, Query(ge=1, le=1000)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    db: AsyncSession = Depends(get_db),
):
    """Получить список всех прайсов с фильтрацией."""
    queries = PriceComposition.build_price_queries(db)
    results, total = await queries.list_prices(
        category=category,
        supplier=supplier,
        region=region,
        limit=limit,
        offset=offset,
    )
    return api_response(PaginatedDataSchema(
        items=[
            PriceResponse(
                id=r.id,
                category=r.category,
                supplier=r.supplier,
                region=r.region,
                price_text=r.price_text,
            )
            for r in results
        ],
        total=total,
    ))


@price_q_router.get(
    path='/{price_id}',
    response_model=PriceResponse,
    dependencies=[Depends(require_permissions("pricing_engine:view"))],
)
async def get_price(
    price_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Получить прайс по ID."""
    queries = PriceComposition.build_price_queries(db)
    result = await queries.get_price(price_id)
    return api_response(PriceResponse(
        id=result.id,
        category=result.category,
        supplier=result.supplier,
        region=result.region,
        price_text=result.price_text,
    ))
