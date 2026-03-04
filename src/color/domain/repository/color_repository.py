from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from src.color.domain.aggregates.color import ColorAggregate, ColorAssignAggregate


class ColorRepository(ABC):
    """Репозиторий для работы с цветами"""

    @abstractmethod
    async def get(self, name: str) -> Optional[ColorAggregate]:
        """Получить цвет по имени"""
        pass

    @abstractmethod
    async def list(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> Tuple[List[ColorAggregate], int]:
        """Получить список всех цветов с пагинацией"""
        pass

    @abstractmethod
    async def save(self, aggregate: ColorAggregate) -> ColorAggregate:
        """Сохранить цвет (обновление)"""
        pass

    @abstractmethod
    async def create(self, aggregate: ColorAggregate) -> ColorAggregate:
        """Создать новый цвет"""
        pass

    @abstractmethod
    async def delete(self, name: str) -> bool:
        """Удалить цвет по имени"""
        pass


class ColorAssignRepository(ABC):
    """Репозиторий для работы с назначениями цветов"""

    @abstractmethod
    async def get(self, assign_id: int) -> Optional[ColorAssignAggregate]:
        """Получить назначение по ID"""
        pass

    @abstractmethod
    async def list(
        self,
        color: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Tuple[List[ColorAssignAggregate], int]:
        """Получить список всех назначений с пагинацией"""
        pass

    @abstractmethod
    async def create(
        self,
        key: str,
        color: str,
    ) -> ColorAssignAggregate:
        """Создать новое назначение"""
        pass

    @abstractmethod
    async def update(
        self,
        assign_id: int,
        key: Optional[str] = None,
        color: Optional[str] = None,
    ) -> ColorAssignAggregate:
        """Обновить назначение"""
        pass

    @abstractmethod
    async def delete(self, assign_id: int) -> bool:
        """Удалить назначение по ID"""
        pass
