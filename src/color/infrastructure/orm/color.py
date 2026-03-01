from typing import List, Optional

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.color.domain.aggregates.color import ColorAggregate, ColorAssignAggregate
from src.color.domain.repository.color_repository import (
    ColorAssignRepository,
    ColorRepository,
)
from src.color.infrastructure.models.color import Color, ColorAssign


class SqlAlchemyColorRepository(ColorRepository):
    """SQLAlchemy реализация репозитория цветов"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, name: str) -> Optional[ColorAggregate]:
        """Получить цвет по имени"""
        query = select(Color).where(Color.name == name)
        result = await self.db.execute(query)
        color = result.scalar_one_or_none()
        if color:
            return ColorAggregate(name=color.name)
        return None

    async def list(self) -> List[ColorAggregate]:
        """Получить список всех цветов"""
        query = select(Color).order_by(Color.name)
        result = await self.db.execute(query)
        colors = result.scalars().all()
        return [ColorAggregate(name=color.name) for color in colors]

    async def save(self, aggregate: ColorAggregate) -> ColorAggregate:
        """Сохранить цвет (обновление)"""
        query = (
            update(Color)
            .where(Color.name == aggregate.name)
            .values(name=aggregate.name)
        )
        await self.db.execute(query)
        await self.db.commit()
        return aggregate

    async def create(self, aggregate: ColorAggregate) -> ColorAggregate:
        """Создать новый цвет"""
        color = Color(name=aggregate.name)
        self.db.add(color)
        await self.db.commit()
        await self.db.refresh(color)
        return ColorAggregate(name=color.name)

    async def delete(self, name: str) -> bool:
        """Удалить цвет по имени"""
        query = delete(Color).where(Color.name == name)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0


class SqlAlchemyColorAssignRepository(ColorAssignRepository):
    """SQLAlchemy реализация репозитория назначений цветов"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, assign_id: int) -> Optional[ColorAssignAggregate]:
        """Получить назначение по ID"""
        query = select(ColorAssign).where(ColorAssign.id == assign_id)
        result = await self.db.execute(query)
        assign = result.scalar_one_or_none()
        if assign:
            return ColorAssignAggregate(
                id=assign.id,
                key=assign.key,
                color=assign.color,
            )
        return None

    async def list(self, color: Optional[str] = None) -> List[ColorAssignAggregate]:
        """Получить список всех назначений"""
        query = select(ColorAssign).order_by(ColorAssign.id)
        if color:
            query = query.where(ColorAssign.color == color)
        result = await self.db.execute(query)
        assigns = result.scalars().all()
        return [
            ColorAssignAggregate(
                id=assign.id,
                key=assign.key,
                color=assign.color,
            )
            for assign in assigns
        ]

    async def create(
        self,
        key: str,
        color: str,
    ) -> ColorAssignAggregate:
        """Создать новое назначение"""
        assign = ColorAssign(key=key, color=color)
        self.db.add(assign)
        await self.db.commit()
        await self.db.refresh(assign)
        return ColorAssignAggregate(
            id=assign.id,
            key=assign.key,
            color=assign.color,
        )

    async def update(
        self,
        assign_id: int,
        key: Optional[str] = None,
        color: Optional[str] = None,
    ) -> ColorAssignAggregate:
        """Обновить назначение"""
        values = {}
        if key is not None:
            values["key"] = key
        if color is not None:
            values["color"] = color

        query = (
            update(ColorAssign)
            .where(ColorAssign.id == assign_id)
            .values(**values)
            .returning(ColorAssign)
        )
        result = await self.db.execute(query)
        await self.db.commit()
        assign = result.scalar_one_or_none()
        if assign:
            return ColorAssignAggregate(
                id=assign.id,
                key=assign.key,
                color=assign.color,
            )
        raise ValueError(f"ColorAssign with id {assign_id} not found")

    async def delete(self, assign_id: int) -> bool:
        """Удалить назначение по ID"""
        query = delete(ColorAssign).where(ColorAssign.id == assign_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
