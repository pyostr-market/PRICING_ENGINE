from src.color.application.dto.color import ColorDTO
from src.color.domain.aggregates.color import ColorAggregate
from src.color.domain.repository.color_repository import ColorRepository
from src.core.auth.schemas.user import User
from src.core.db.unit_of_work import UnitOfWork
from src.core.events import AsyncEventBus, build_event


class CreateColorCommand:
    """Команда создания цвета"""

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
        dto: ColorDTO,
        user: User,
    ) -> ColorDTO:
        """Создать новый цвет"""
        # Проверяем, существует ли уже цвет с таким именем
        existing = await self.repository.get(dto.name)
        if existing:
            from src.core.exceptions.service_errors import ColorAlreadyExistsError
            raise ColorAlreadyExistsError(dto.name)

        # Создаем агрегат и сохраняем
        aggregate = ColorAggregate(name=dto.name)
        async with self.uow:
            created = await self.repository.create(aggregate)

        # Публикуем событие
        self.event_bus.publish_nowait(
            build_event(
                event_type="created",
                method="create_color",
                app="pricing_engine",
                entity="color",
                entity_id=None,
                data={"name": created.name},
            )
        )

        return ColorDTO(name=created.name)
