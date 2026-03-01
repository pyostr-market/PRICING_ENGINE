from src.color.application.dto.color import ColorDTO
from src.color.domain.aggregates.color import ColorAggregate
from src.color.domain.repository.color_repository import ColorRepository
from src.core.auth.schemas.user import User
from src.core.db.unit_of_work import UnitOfWork
from src.core.events import AsyncEventBus, build_event


class UpdateColorCommand:
    """Команда обновления цвета"""

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
        dto: ColorDTO,
        user: User,
    ) -> ColorDTO:
        """Обновить существующий цвет"""
        # Проверяем, существует ли цвет
        existing = await self.repository.get(name)
        if not existing:
            from src.core.exceptions.service_errors import ColorNotFoundError
            raise ColorNotFoundError(name)

        # Если имя меняется, проверяем, не занято ли новое имя
        if dto.name != name:
            existing_new_name = await self.repository.get(dto.name)
            if existing_new_name:
                from src.core.exceptions.service_errors import ColorAlreadyExistsError
                raise ColorAlreadyExistsError(dto.name)

        # Обновляем цвет
        aggregate = ColorAggregate(name=dto.name)
        async with self.uow:
            await self.repository.save(aggregate)

        # Публикуем событие
        self.event_bus.publish_nowait(
            build_event(
                event_type="updated",
                method="update_color",
                app="pricing_engine",
                entity="color",
                entity_id=None,
                data={"old_name": name, "new_name": dto.name},
            )
        )

        return ColorDTO(name=dto.name)
