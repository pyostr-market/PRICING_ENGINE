from typing import List, Optional, Tuple

from src.price.application.dto.price import PriceDTO
from src.price.domain.repository.price_repository import PriceRepository


class PriceQueries:
    """Запросы для получения данных о прайсах"""

    def __init__(
        self,
        repository: PriceRepository,
    ):
        self.repository = repository

    async def get_price(self, price_id: int) -> PriceDTO:
        """Получить прайс по ID"""
        price = await self.repository.get(price_id)
        if not price:
            from src.core.exceptions.service_errors import PriceNotFoundError
            raise PriceNotFoundError(price_id)
        return PriceDTO(
            id=price.id,
            category=price.category,
            supplier=price.supplier,
            region=price.region,
            price_text=price.price_text,
        )

    async def list_prices(
        self,
        category: Optional[str] = None,
        supplier: Optional[str] = None,
        region: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Tuple[List[PriceDTO], int]:
        """Получить список всех прайсов с пагинацией"""
        prices, total = await self.repository.list(
            category=category,
            supplier=supplier,
            region=region,
            limit=limit,
            offset=offset,
        )
        return [
            PriceDTO(
                id=price.id,
                category=price.category,
                supplier=price.supplier,
                region=price.region,
                price_text=price.price_text,
            )
            for price in prices
        ], total
