from src.color.domain.repository.color_repository import ColorAssignRepository
from src.core.auth.schemas.user import User
from src.core.db.unit_of_work import UnitOfWork
from src.core.events import AsyncEventBus, build_event


class DeleteColorAssignCommand:
    """Команда удаления назначения цвета"""

    def __init__(
        self,
        repository: ColorAssignRepository,
        uow: UnitOfWork,
        event_bus: AsyncEventBus,
    ):
        self.repository = repository
        self.uow = uow
        self.event_bus = event_bus

    async def execute(
        self,
        assign_id: int,
        user: User,
    ) -> bool:
        """Удалить назначение цвета"""
        # Проверяем, существует ли назначение
        existing = await self.repository.get(assign_id)
        if not existing:
            from src.core.exceptions.service_errors import ColorAssignNotFoundError
            raise ColorAssignNotFoundError(assign_id)

        async with self.uow:
            deleted = await self.repository.delete(assign_id)

        # Публикуем событие
        self.event_bus.publish_nowait(
            build_event(
                event_type="deleted",
                method="delete_color_assign",
                app="pricing_engine",
                entity="color_assign",
                entity_id=assign_id,
                data={"id": assign_id},
            )
        )

        return deleted
