from sqlalchemy.exc import IntegrityError

from src.color.application.dto.color import ColorAssignDTO, ColorAssignUpdateDTO
from src.color.domain.repository.color_repository import ColorAssignRepository
from src.core.auth.schemas.user import User
from src.core.db.unit_of_work import UnitOfWork
from src.core.events import AsyncEventBus, build_event
from src.core.exceptions.service_errors import (
    ColorAssignForeignKeyViolationError,
    ColorAssignNotFoundError,
)


class UpdateColorAssignCommand:
    """Команда обновления назначения цвета"""

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
        dto: ColorAssignUpdateDTO,
        user: User,
    ) -> ColorAssignDTO:
        """Обновить назначение цвета"""
        # Проверяем, существует ли назначение
        existing = await self.repository.get(assign_id)
        if not existing:
            raise ColorAssignNotFoundError(assign_id)

        try:
            async with self.uow:
                updated = await self.repository.update(
                    assign_id=assign_id,
                    key=dto.key,
                    color=dto.color,
                )
        except IntegrityError as e:
            error_str = str(e.orig).lower()
            if "foreign key" in error_str:
                raise ColorAssignForeignKeyViolationError(color=dto.color or existing.color) from e
            raise

        # Публикуем событие
        self.event_bus.publish_nowait(
            build_event(
                event_type="updated",
                method="update_color_assign",
                app="pricing_engine",
                entity="color_assign",
                entity_id=updated.id,
                data={"key": updated.key, "color": updated.color},
            )
        )

        return ColorAssignDTO(
            id=updated.id,
            key=updated.key,
            color=updated.color,
        )
