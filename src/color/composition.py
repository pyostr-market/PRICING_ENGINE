from sqlalchemy.ext.asyncio import AsyncSession

from src.color.application.commands.color_assign.create_color_assign import (
    CreateColorAssignCommand,
)
from src.color.application.commands.color_assign.delete_color_assign import (
    DeleteColorAssignCommand,
)
from src.color.application.commands.color_assign.update_color_assign import (
    UpdateColorAssignCommand,
)
from src.color.application.commands.create_color import CreateColorCommand
from src.color.application.commands.delete_color import DeleteColorCommand
from src.color.application.commands.update_color import UpdateColorCommand
from src.color.application.queries.color import ColorAssignQueries, ColorQueries
from src.color.container import container


class ColorComposition:
    """Композиция для модуля Color"""

    @staticmethod
    def build_create_color_command(db: AsyncSession) -> CreateColorCommand:
        scope = container.create_scope()
        return scope.resolve(CreateColorCommand, db=db)

    @staticmethod
    def build_update_color_command(db: AsyncSession) -> UpdateColorCommand:
        scope = container.create_scope()
        return scope.resolve(UpdateColorCommand, db=db)

    @staticmethod
    def build_delete_color_command(db: AsyncSession) -> DeleteColorCommand:
        scope = container.create_scope()
        return scope.resolve(DeleteColorCommand, db=db)

    @staticmethod
    def build_color_queries(db: AsyncSession) -> ColorQueries:
        scope = container.create_scope()
        return scope.resolve(ColorQueries, db=db)

    @staticmethod
    def build_create_color_assign_command(db: AsyncSession) -> CreateColorAssignCommand:
        scope = container.create_scope()
        return scope.resolve(CreateColorAssignCommand, db=db)

    @staticmethod
    def build_update_color_assign_command(db: AsyncSession) -> UpdateColorAssignCommand:
        scope = container.create_scope()
        return scope.resolve(UpdateColorAssignCommand, db=db)

    @staticmethod
    def build_delete_color_assign_command(db: AsyncSession) -> DeleteColorAssignCommand:
        scope = container.create_scope()
        return scope.resolve(DeleteColorAssignCommand, db=db)

    @staticmethod
    def build_color_assign_queries(db: AsyncSession) -> ColorAssignQueries:
        scope = container.create_scope()
        return scope.resolve(ColorAssignQueries, db=db)
