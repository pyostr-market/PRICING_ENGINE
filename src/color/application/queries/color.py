from typing import List, Optional

from src.color.application.dto.color import ColorAssignDTO, ColorDTO
from src.color.domain.repository.color_repository import (
    ColorAssignRepository,
    ColorRepository,
)


class ColorQueries:
    """Запросы для получения данных о цветах"""

    def __init__(
        self,
        repository: ColorRepository,
    ):
        self.repository = repository

    async def get_color(self, name: str) -> ColorDTO:
        """Получить цвет по имени"""
        color = await self.repository.get(name)
        if not color:
            from src.core.exceptions.service_errors import ColorNotFoundError
            raise ColorNotFoundError(name)
        return ColorDTO(name=color.name)

    async def list_colors(self) -> List[ColorDTO]:
        """Получить список всех цветов"""
        colors = await self.repository.list()
        return [ColorDTO(name=color.name) for color in colors]


class ColorAssignQueries:
    """Запросы для получения данных о назначениях цветов"""

    def __init__(
        self,
        repository: ColorAssignRepository,
    ):
        self.repository = repository

    async def get_color_assign(self, assign_id: int) -> ColorAssignDTO:
        """Получить назначение по ID"""
        assign = await self.repository.get(assign_id)
        if not assign:
            from src.core.exceptions.service_errors import ColorAssignNotFoundError
            raise ColorAssignNotFoundError(assign_id)
        return ColorAssignDTO(
            id=assign.id,
            key=assign.key,
            color=assign.color,
        )

    async def list_color_assigns(
        self,
        color: Optional[str] = None,
    ) -> List[ColorAssignDTO]:
        """Получить список всех назначений"""
        assigns = await self.repository.list(color=color)
        return [
            ColorAssignDTO(
                id=assign.id,
                key=assign.key,
                color=assign.color,
            )
            for assign in assigns
        ]
