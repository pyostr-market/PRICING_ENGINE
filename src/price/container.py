from src.price.application.commands.create_price import CreatePriceCommand
from src.price.application.commands.delete_price import DeletePriceCommand
from src.price.application.commands.update_price import UpdatePriceCommand
from src.price.application.queries.price import PriceQueries
from src.price.domain.repository.price_repository import (
    PriceRepository,
    CategoryRepository,
    SupplierRepository,
    RegionRepository,
)
from src.price.infrastructure.orm.price import (
    SqlAlchemyPriceRepository,
    SqlAlchemyCategoryRepository,
    SqlAlchemySupplierRepository,
    SqlAlchemyRegionRepository,
)
from src.core.db.unit_of_work import UnitOfWork
from src.core.di.container import ServiceContainer
from src.core.events import AsyncEventBus, get_event_bus

container = ServiceContainer()

# === Repositories ===
container.register(
    CategoryRepository,
    lambda scope, db: SqlAlchemyCategoryRepository(db),
)

container.register(
    SupplierRepository,
    lambda scope, db: SqlAlchemySupplierRepository(db),
)

container.register(
    RegionRepository,
    lambda scope, db: SqlAlchemyRegionRepository(db),
)

container.register(
    PriceRepository,
    lambda scope, db: SqlAlchemyPriceRepository(db),
)

container.register(
    UnitOfWork,
    lambda scope, db: UnitOfWork(db),
)

container.register(
    AsyncEventBus,
    lambda scope, db: get_event_bus(),
)

# === Queries ===
container.register(
    PriceQueries,
    lambda scope, db: PriceQueries(
        repository=scope.resolve(PriceRepository, db=db),
    ),
)

# === Commands ===
container.register(
    CreatePriceCommand,
    lambda scope, db: CreatePriceCommand(
        repository=scope.resolve(PriceRepository, db=db),
        category_repository=scope.resolve(CategoryRepository, db=db),
        supplier_repository=scope.resolve(SupplierRepository, db=db),
        region_repository=scope.resolve(RegionRepository, db=db),
        uow=scope.resolve(UnitOfWork, db=db),
        event_bus=scope.resolve(AsyncEventBus, db=db),
    ),
)

container.register(
    UpdatePriceCommand,
    lambda scope, db: UpdatePriceCommand(
        repository=scope.resolve(PriceRepository, db=db),
        category_repository=scope.resolve(CategoryRepository, db=db),
        supplier_repository=scope.resolve(SupplierRepository, db=db),
        region_repository=scope.resolve(RegionRepository, db=db),
        uow=scope.resolve(UnitOfWork, db=db),
        event_bus=scope.resolve(AsyncEventBus, db=db),
    ),
)

container.register(
    DeletePriceCommand,
    lambda scope, db: DeletePriceCommand(
        repository=scope.resolve(PriceRepository, db=db),
        uow=scope.resolve(UnitOfWork, db=db),
        event_bus=scope.resolve(AsyncEventBus, db=db),
    ),
)
