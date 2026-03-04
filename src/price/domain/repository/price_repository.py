from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from src.price.domain.aggregates.price import (
    CategoryAggregate,
    SupplierAggregate,
    RegionAggregate,
    PriceAggregate,
)


class CategoryRepository(ABC):
    """Репозиторий для работы с категориями"""

    @abstractmethod
    async def get(self, name: str) -> Optional[CategoryAggregate]:
        """Получить категорию по имени"""
        pass

    @abstractmethod
    async def list(self) -> List[CategoryAggregate]:
        """Получить список всех категорий"""
        pass

    @abstractmethod
    async def save(self, aggregate: CategoryAggregate) -> CategoryAggregate:
        """Сохранить категорию (обновление)"""
        pass

    @abstractmethod
    async def create(self, aggregate: CategoryAggregate) -> CategoryAggregate:
        """Создать новую категорию"""
        pass

    @abstractmethod
    async def delete(self, name: str) -> bool:
        """Удалить категорию по имени"""
        pass


class SupplierRepository(ABC):
    """Репозиторий для работы с поставщиками"""

    @abstractmethod
    async def get(self, name: str) -> Optional[SupplierAggregate]:
        """Получить поставщика по имени"""
        pass

    @abstractmethod
    async def list(self) -> List[SupplierAggregate]:
        """Получить список всех поставщиков"""
        pass

    @abstractmethod
    async def save(self, aggregate: SupplierAggregate) -> SupplierAggregate:
        """Сохранить поставщика (обновление)"""
        pass

    @abstractmethod
    async def create(self, aggregate: SupplierAggregate) -> SupplierAggregate:
        """Создать нового поставщика"""
        pass

    @abstractmethod
    async def delete(self, name: str) -> bool:
        """Удалить поставщика по имени"""
        pass


class RegionRepository(ABC):
    """Репозиторий для работы с регионами"""

    @abstractmethod
    async def get(self, name: str) -> Optional[RegionAggregate]:
        """Получить регион по имени"""
        pass

    @abstractmethod
    async def list(self) -> List[RegionAggregate]:
        """Получить список всех регионов"""
        pass

    @abstractmethod
    async def save(self, aggregate: RegionAggregate) -> RegionAggregate:
        """Сохранить регион (обновление)"""
        pass

    @abstractmethod
    async def create(self, aggregate: RegionAggregate) -> RegionAggregate:
        """Создать новый регион"""
        pass

    @abstractmethod
    async def delete(self, name: str) -> bool:
        """Удалить регион по имени"""
        pass


class PriceRepository(ABC):
    """Репозиторий для работы с прайсами"""

    @abstractmethod
    async def get(self, price_id: int) -> Optional[PriceAggregate]:
        """Получить прайс по ID"""
        pass

    @abstractmethod
    async def list(
        self,
        category: Optional[str] = None,
        supplier: Optional[str] = None,
        region: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Tuple[List[PriceAggregate], int]:
        """Получить список всех прайсов с пагинацией"""
        pass

    @abstractmethod
    async def create(
        self,
        category: str,
        supplier: str,
        region: str,
        price_text: str,
    ) -> PriceAggregate:
        """Создать новый прайс"""
        pass

    @abstractmethod
    async def update(
        self,
        price_id: int,
        category: Optional[str] = None,
        supplier: Optional[str] = None,
        region: Optional[str] = None,
        price_text: Optional[str] = None,
    ) -> PriceAggregate:
        """Обновить прайс"""
        pass

    @abstractmethod
    async def delete(self, price_id: int) -> bool:
        """Удалить прайс по ID"""
        pass
