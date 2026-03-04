from src.price.domain.repository.price_repository import PriceRepository
from src.core.auth.schemas.user import User
from src.core.db.unit_of_work import UnitOfWork
from src.core.events import AsyncEventBus, build_event


class DeletePriceCommand:
    """Команда удаления прайса"""

    def __init__(
        self,
        repository: PriceRepository,
        uow: UnitOfWork,
        event_bus: AsyncEventBus,
    ):
        self.repository = repository
        self.uow = uow
        self.event_bus = event_bus

    async def execute(
        self,
        price_id: int,
        user: User,
    ) -> bool:
        """Удалить прайс"""
        # Проверяем, существует ли прайс
        existing = await self.repository.get(price_id)
        if not existing:
            from src.core.exceptions.service_errors import PriceNotFoundError
            raise PriceNotFoundError(price_id)

        async with self.uow:
            deleted = await self.repository.delete(price_id)

        # Публикуем событие
        self.event_bus.publish_nowait(
            build_event(
                event_type="deleted",
                method="delete_price",
                app="pricing_engine",
                entity="price",
                entity_id=price_id,
                data={"id": price_id},
            )
        )

        return deleted
