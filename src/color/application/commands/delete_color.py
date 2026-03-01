from src.color.domain.repository.color_repository import ColorRepository
from src.core.auth.schemas.user import User
from src.core.db.unit_of_work import UnitOfWork
from src.core.events import AsyncEventBus, build_event


class DeleteColorCommand:
    """Команда удаления цвета"""

    def __init__(
        self,
        repository: ColorRepository,
        uow: UnitOfWork,
        event_bus: AsyncEventBus,
    ):
        self.repository = repository
        self.uow = uow
        self.event_bus = event_bus

    async def execute(
        self,
        name: str,
        user: User,
    ) -> bool:
        """Удалить цвет"""
        # Проверяем, существует ли цвет
        existing = await self.repository.get(name)
        if not existing:
            from src.core.exceptions.service_errors import ColorNotFoundError
            raise ColorNotFoundError(name)

        # Удаляем цвет
        async with self.uow:
            deleted = await self.repository.delete(name)

        # Публикуем событие
        self.event_bus.publish_nowait(
            build_event(
                event_type="deleted",
                method="delete_color",
                app="pricing_engine",
                entity="color",
                entity_id=None,
                data={"name": name},
            )
        )

        return deleted
