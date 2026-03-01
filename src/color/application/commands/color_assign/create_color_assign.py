from sqlalchemy.exc import IntegrityError

from src.color.application.dto.color import ColorAssignCreateDTO, ColorAssignDTO
from src.color.domain.repository.color_repository import ColorAssignRepository
from src.core.auth.schemas.user import User
from src.core.db.unit_of_work import UnitOfWork
from src.core.events import AsyncEventBus, build_event
from src.core.exceptions.service_errors import ColorAssignForeignKeyViolationError


class CreateColorAssignCommand:
    """Команда создания назначения цвета"""

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
        dto: ColorAssignCreateDTO,
        user: User,
    ) -> ColorAssignDTO:
        """Создать новое назначение цвета"""
        try:
            async with self.uow:
                created = await self.repository.create(
                    key=dto.key,
                    color=dto.color,
                )
        except IntegrityError as e:
            error_str = str(e.orig).lower()
            if "foreign key" in error_str:
                raise ColorAssignForeignKeyViolationError(color=dto.color) from e
            if "unique" in error_str or "duplicate" in error_str:
                from src.core.exceptions.service_errors import ColorAssignAlreadyExistsError
                raise ColorAssignAlreadyExistsError(key=dto.key, color=dto.color) from e
            raise

        # Публикуем событие
        self.event_bus.publish_nowait(
            build_event(
                event_type="created",
                method="create_color_assign",
                app="pricing_engine",
                entity="color_assign",
                entity_id=created.id,
                data={"key": created.key, "color": created.color},
            )
        )

        return ColorAssignDTO(
            id=created.id,
            key=created.key,
            color=created.color,
        )
