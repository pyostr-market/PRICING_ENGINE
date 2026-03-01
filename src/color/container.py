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
from src.color.domain.repository.color_repository import (
    ColorAssignRepository,
    ColorRepository,
)
from src.color.infrastructure.orm.color import (
    SqlAlchemyColorAssignRepository,
    SqlAlchemyColorRepository,
)
from src.core.db.unit_of_work import UnitOfWork
from src.core.di.container import ServiceContainer
from src.core.events import AsyncEventBus, get_event_bus

container = ServiceContainer()

# === Repositories ===
container.register(
    ColorRepository,
    lambda scope, db: SqlAlchemyColorRepository(db),
)

container.register(
    ColorAssignRepository,
    lambda scope, db: SqlAlchemyColorAssignRepository(db),
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
    ColorQueries,
    lambda scope, db: ColorQueries(
        repository=scope.resolve(ColorRepository, db=db),
    ),
)

container.register(
    ColorAssignQueries,
    lambda scope, db: ColorAssignQueries(
        repository=scope.resolve(ColorAssignRepository, db=db),
    ),
)

# === Commands ===
container.register(
    CreateColorCommand,
    lambda scope, db: CreateColorCommand(
        repository=scope.resolve(ColorRepository, db=db),
        uow=scope.resolve(UnitOfWork, db=db),
        event_bus=scope.resolve(AsyncEventBus, db=db),
    ),
)

container.register(
    UpdateColorCommand,
    lambda scope, db: UpdateColorCommand(
        repository=scope.resolve(ColorRepository, db=db),
        uow=scope.resolve(UnitOfWork, db=db),
        event_bus=scope.resolve(AsyncEventBus, db=db),
    ),
)

container.register(
    DeleteColorCommand,
    lambda scope, db: DeleteColorCommand(
        repository=scope.resolve(ColorRepository, db=db),
        uow=scope.resolve(UnitOfWork, db=db),
        event_bus=scope.resolve(AsyncEventBus, db=db),
    ),
)

container.register(
    CreateColorAssignCommand,
    lambda scope, db: CreateColorAssignCommand(
        repository=scope.resolve(ColorAssignRepository, db=db),
        uow=scope.resolve(UnitOfWork, db=db),
        event_bus=scope.resolve(AsyncEventBus, db=db),
    ),
)

container.register(
    UpdateColorAssignCommand,
    lambda scope, db: UpdateColorAssignCommand(
        repository=scope.resolve(ColorAssignRepository, db=db),
        uow=scope.resolve(UnitOfWork, db=db),
        event_bus=scope.resolve(AsyncEventBus, db=db),
    ),
)

container.register(
    DeleteColorAssignCommand,
    lambda scope, db: DeleteColorAssignCommand(
        repository=scope.resolve(ColorAssignRepository, db=db),
        uow=scope.resolve(UnitOfWork, db=db),
        event_bus=scope.resolve(AsyncEventBus, db=db),
    ),
)
