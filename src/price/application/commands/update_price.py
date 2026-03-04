from sqlalchemy.exc import IntegrityError

from src.price.application.dto.price import PriceDTO, PriceUpdateDTO
from src.price.domain.aggregates.price import (
    CategoryAggregate,
    SupplierAggregate,
    RegionAggregate,
)
from src.price.domain.repository.price_repository import (
    PriceRepository,
    CategoryRepository,
    SupplierRepository,
    RegionRepository,
)
from src.core.auth.schemas.user import User
from src.core.db.unit_of_work import UnitOfWork
from src.core.events import AsyncEventBus, build_event
from src.core.exceptions.service_errors import (
    PriceForeignKeyViolationError,
    PriceNotFoundError,
)


class UpdatePriceCommand:
    """Команда обновления прайса"""

    def __init__(
        self,
        repository: PriceRepository,
        category_repository: CategoryRepository,
        supplier_repository: SupplierRepository,
        region_repository: RegionRepository,
        uow: UnitOfWork,
        event_bus: AsyncEventBus,
    ):
        self.repository = repository
        self.category_repository = category_repository
        self.supplier_repository = supplier_repository
        self.region_repository = region_repository
        self.uow = uow
        self.event_bus = event_bus

    async def execute(
        self,
        price_id: int,
        dto: PriceUpdateDTO,
        user: User,
    ) -> PriceDTO:
        """Обновить прайс. Если категория, поставщик или регион не существуют - создаем их."""
        try:
            async with self.uow:
                # Проверяем, существует ли прайс
                existing = await self.repository.get(price_id)
                if not existing:
                    raise PriceNotFoundError(price_id)

                # Определяем значения для проверки/создания справочников
                category_name = (dto.category.lower() if dto.category else existing.category)
                supplier_name = (dto.supplier.lower() if dto.supplier else existing.supplier)
                region_name = (dto.region.lower() if dto.region else existing.region)

                # Проверяем и создаем категорию если нужно
                category = await self.category_repository.get(category_name)
                if not category:
                    await self.category_repository.create(
                        CategoryAggregate(name=category_name)
                    )

                # Проверяем и создаем поставщика если нужно
                supplier = await self.supplier_repository.get(supplier_name)
                if not supplier:
                    await self.supplier_repository.create(
                        SupplierAggregate(name=supplier_name)
                    )

                # Проверяем и создаем регион если нужно
                region = await self.region_repository.get(region_name)
                if not region:
                    await self.region_repository.create(
                        RegionAggregate(name=region_name)
                    )

                # Делаем flush, чтобы справочники сохранились в БД перед обновлением прайса
                await self.uow.session.flush()

                updated = await self.repository.update(
                    price_id=price_id,
                    category=category_name if dto.category else None,
                    supplier=supplier_name if dto.supplier else None,
                    region=region_name if dto.region else None,
                    price_text=dto.price_text,
                )

                # Публикуем событие
                self.event_bus.publish_nowait(
                    build_event(
                        event_type="updated",
                        method="update_price",
                        app="pricing_engine",
                        entity="price",
                        entity_id=updated.id,
                        data={
                            "category": updated.category,
                            "supplier": updated.supplier,
                            "region": updated.region,
                        },
                    )
                )

                return PriceDTO(
                    id=updated.id,
                    category=updated.category,
                    supplier=updated.supplier,
                    region=updated.region,
                    price_text=updated.price_text,
                )
        except IntegrityError as e:
            error_str = str(e.orig).lower()
            if "foreign key" in error_str:
                raise PriceForeignKeyViolationError from e
            if "unique" in error_str or "duplicate" in error_str:
                from src.core.exceptions.service_errors import PriceAlreadyExistsError
                raise PriceAlreadyExistsError(
                    category=category_name,
                    supplier=supplier_name,
                    region=region_name,
                ) from e
            raise
