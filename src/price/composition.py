from sqlalchemy.ext.asyncio import AsyncSession

from src.price.application.commands.create_price import CreatePriceCommand
from src.price.application.commands.delete_price import DeletePriceCommand
from src.price.application.commands.update_price import UpdatePriceCommand
from src.price.application.queries.price import PriceQueries
from src.price.container import container


class PriceComposition:
    """Композиция для модуля Price"""

    @staticmethod
    def build_create_price_command(db: AsyncSession) -> CreatePriceCommand:
        scope = container.create_scope()
        return scope.resolve(CreatePriceCommand, db=db)

    @staticmethod
    def build_update_price_command(db: AsyncSession) -> UpdatePriceCommand:
        scope = container.create_scope()
        return scope.resolve(UpdatePriceCommand, db=db)

    @staticmethod
    def build_delete_price_command(db: AsyncSession) -> DeletePriceCommand:
        scope = container.create_scope()
        return scope.resolve(DeletePriceCommand, db=db)

    @staticmethod
    def build_price_queries(db: AsyncSession) -> PriceQueries:
        scope = container.create_scope()
        return scope.resolve(PriceQueries, db=db)
