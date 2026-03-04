from sqlalchemy.exc import IntegrityError

from src.price.application.dto.price import PriceCreateDTO, PriceDTO
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
from src.core.exceptions.service_errors import PriceForeignKeyViolationError


class CreatePriceCommand:
    """Команда создания прайса"""

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
        dto: PriceCreateDTO,
        user: User,
    ) -> PriceDTO:
        """Создать новый прайс. Если категория, поставщик или регион не существуют - создаем их."""
        try:
            async with self.uow:
                # Нормализуем названия (приводим к lowercase, как в моделях)
                category_name = dto.category.lower()
                supplier_name = dto.supplier.lower()
                region_name = dto.region.lower()

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

                # Делаем flush, чтобы справочники сохранились в БД перед созданием прайса
                await self.uow.session.flush()

                created = await self.repository.create(
                    category=category_name,
                    supplier=supplier_name,
                    region=region_name,
                    price_text=dto.price_text,
                )

                # Публикуем событие
                self.event_bus.publish_nowait(
                    build_event(
                        event_type="created",
                        method="create_price",
                        app="pricing_engine",
                        entity="price",
                        entity_id=created.id,
                        data={
                            "category": created.category,
                            "supplier": created.supplier,
                            "region": created.region,
                        },
                    )
                )

                return PriceDTO(
                    id=created.id,
                    category=created.category,
                    supplier=created.supplier,
                    region=created.region,
                    price_text=created.price_text,
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
