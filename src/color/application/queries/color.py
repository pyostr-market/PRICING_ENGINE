from typing import List, Optional, Tuple

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

    async def list_colors(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> Tuple[List[ColorDTO], int]:
        """Получить список всех цветов с пагинацией"""
        colors, total = await self.repository.list(limit=limit, offset=offset)
        return [ColorDTO(name=color.name) for color in colors], total


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
        limit: int = 100,
        offset: int = 0,
    ) -> Tuple[List[ColorAssignDTO], int]:
        """Получить список всех назначений с пагинацией"""
        assigns, total = await self.repository.list(color=color, limit=limit, offset=offset)
        return [
            ColorAssignDTO(
                id=assign.id,
                key=assign.key,
                color=assign.color,
            )
            for assign in assigns
        ], total
