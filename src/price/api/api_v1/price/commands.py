from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.price.api.api_v1.price.schemas import (
    PriceCreateRequest,
    PriceResponse,
    PriceUpdateRequest,
)
from src.price.application.dto.price import PriceCreateDTO, PriceUpdateDTO
from src.price.composition import PriceComposition
from src.core.api.responses import api_response
from src.core.auth.dependencies import get_current_user, require_permissions
from src.core.auth.schemas.user import User
from src.core.db.database import get_db

price_commands_router = APIRouter(
    tags=["Прайсы"],
)


@price_commands_router.post(
    path='/',
    response_model=PriceResponse,
    dependencies=[Depends(require_permissions("pricing_engine:create"))],
)
async def create_price(
    request: PriceCreateRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Создать новый прайс. Если категория, поставщик или регион не существуют - они будут созданы."""
    dto = PriceCreateDTO(
        category=request.category,
        supplier=request.supplier,
        region=request.region,
        price_text=request.price_text,
    )
    command = PriceComposition.build_create_price_command(db)
    result = await command.execute(dto, user)
    return api_response(PriceResponse(
        id=result.id,
        category=result.category,
        supplier=result.supplier,
        region=result.region,
        price_text=result.price_text,
    ))


@price_commands_router.put(
    path='/{price_id}',
    response_model=PriceResponse,
    dependencies=[Depends(require_permissions("pricing_engine:update"))],
)
async def update_price(
    price_id: int,
    request: PriceUpdateRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Обновить существующий прайс. Если категория, поставщик или регион не существуют - они будут созданы."""
    dto = PriceUpdateDTO(
        category=request.category,
        supplier=request.supplier,
        region=request.region,
        price_text=request.price_text,
    )
    command = PriceComposition.build_update_price_command(db)
    result = await command.execute(price_id, dto, user)
    return api_response(PriceResponse(
        id=result.id,
        category=result.category,
        supplier=result.supplier,
        region=result.region,
        price_text=result.price_text,
    ))


@price_commands_router.delete(
    path='/{price_id}',
    dependencies=[Depends(require_permissions("pricing_engine:delete"))],
)
async def delete_price(
    price_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Удалить прайс."""
    command = PriceComposition.build_delete_price_command(db)
    result = await command.execute(price_id, user)
    return api_response({"deleted": result})
