from typing import List, Optional, Tuple

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.price.domain.aggregates.price import (
    CategoryAggregate,
    SupplierAggregate,
    RegionAggregate,
    PriceAggregate,
)
from src.price.domain.repository.price_repository import (
    CategoryRepository,
    SupplierRepository,
    RegionRepository,
    PriceRepository,
)
from src.price.infrastructure.models.price import Category, Supplier, Region, Price


class SqlAlchemyCategoryRepository(CategoryRepository):
    """SQLAlchemy реализация репозитория категорий"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, name: str) -> Optional[CategoryAggregate]:
        """Получить категорию по имени"""
        query = select(Category).where(Category.name == name)
        result = await self.db.execute(query)
        category = result.scalar_one_or_none()
        if category:
            return CategoryAggregate(name=category.name)
        return None

    async def list(self) -> List[CategoryAggregate]:
        """Получить список всех категорий"""
        query = select(Category).order_by(Category.name)
        result = await self.db.execute(query)
        categories = result.scalars().all()
        return [CategoryAggregate(name=cat.name) for cat in categories]

    async def save(self, aggregate: CategoryAggregate) -> CategoryAggregate:
        """Сохранить категорию (обновление)"""
        query = (
            update(Category)
            .where(Category.name == aggregate.name)
            .values(name=aggregate.name)
        )
        await self.db.execute(query)
        return aggregate

    async def create(self, aggregate: CategoryAggregate) -> CategoryAggregate:
        """Создать новую категорию"""
        category = Category(name=aggregate.name)
        self.db.add(category)
        return CategoryAggregate(name=aggregate.name)

    async def delete(self, name: str) -> bool:
        """Удалить категорию по имени"""
        query = delete(Category).where(Category.name == name)
        result = await self.db.execute(query)
        return result.rowcount > 0


class SqlAlchemySupplierRepository(SupplierRepository):
    """SQLAlchemy реализация репозитория поставщиков"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, name: str) -> Optional[SupplierAggregate]:
        """Получить поставщика по имени"""
        query = select(Supplier).where(Supplier.name == name)
        result = await self.db.execute(query)
        supplier = result.scalar_one_or_none()
        if supplier:
            return SupplierAggregate(name=supplier.name)
        return None

    async def list(self) -> List[SupplierAggregate]:
        """Получить список всех поставщиков"""
        query = select(Supplier).order_by(Supplier.name)
        result = await self.db.execute(query)
        suppliers = result.scalars().all()
        return [SupplierAggregate(name=sup.name) for sup in suppliers]

    async def save(self, aggregate: SupplierAggregate) -> SupplierAggregate:
        """Сохранить поставщика (обновление)"""
        query = (
            update(Supplier)
            .where(Supplier.name == aggregate.name)
            .values(name=aggregate.name)
        )
        await self.db.execute(query)
        return aggregate

    async def create(self, aggregate: SupplierAggregate) -> SupplierAggregate:
        """Создать нового поставщика"""
        supplier = Supplier(name=aggregate.name)
        self.db.add(supplier)
        return SupplierAggregate(name=aggregate.name)

    async def delete(self, name: str) -> bool:
        """Удалить поставщика по имени"""
        query = delete(Supplier).where(Supplier.name == name)
        result = await self.db.execute(query)
        return result.rowcount > 0


class SqlAlchemyRegionRepository(RegionRepository):
    """SQLAlchemy реализация репозитория регионов"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, name: str) -> Optional[RegionAggregate]:
        """Получить регион по имени"""
        query = select(Region).where(Region.name == name)
        result = await self.db.execute(query)
        region = result.scalar_one_or_none()
        if region:
            return RegionAggregate(name=region.name)
        return None

    async def list(self) -> List[RegionAggregate]:
        """Получить список всех регионов"""
        query = select(Region).order_by(Region.name)
        result = await self.db.execute(query)
        regions = result.scalars().all()
        return [RegionAggregate(name=reg.name) for reg in regions]

    async def save(self, aggregate: RegionAggregate) -> RegionAggregate:
        """Сохранить регион (обновление)"""
        query = (
            update(Region)
            .where(Region.name == aggregate.name)
            .values(name=aggregate.name)
        )
        await self.db.execute(query)
        return aggregate

    async def create(self, aggregate: RegionAggregate) -> RegionAggregate:
        """Создать новый регион"""
        region = Region(name=aggregate.name)
        self.db.add(region)
        return RegionAggregate(name=aggregate.name)

    async def delete(self, name: str) -> bool:
        """Удалить регион по имени"""
        query = delete(Region).where(Region.name == name)
        result = await self.db.execute(query)
        return result.rowcount > 0


class SqlAlchemyPriceRepository(PriceRepository):
    """SQLAlchemy реализация репозитория прайсов"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, price_id: int) -> Optional[PriceAggregate]:
        """Получить прайс по ID"""
        query = select(Price).where(Price.id == price_id)
        result = await self.db.execute(query)
        price = result.scalar_one_or_none()
        if price:
            return PriceAggregate(
                id=price.id,
                category=price.category,
                supplier=price.supplier,
                region=price.region,
                price_text=price.price_text,
            )
        return None

    async def list(
        self,
        category: Optional[str] = None,
        supplier: Optional[str] = None,
        region: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Tuple[List[PriceAggregate], int]:
        """Получить список всех прайсов с пагинацией"""
        # Базовый запрос
        query = select(Price).order_by(Price.id)
        if category:
            query = query.where(Price.category == category)
        if supplier:
            query = query.where(Price.supplier == supplier)
        if region:
            query = query.where(Price.region == region)
        
        # Получаем общее количество
        count_query = select(func.count()).select_from(Price)
        if category:
            count_query = count_query.where(Price.category == category)
        if supplier:
            count_query = count_query.where(Price.supplier == supplier)
        if region:
            count_query = count_query.where(Price.region == region)
        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0
        
        # Получаем данные с пагинацией
        query = query.offset(offset).limit(limit)
        result = await self.db.execute(query)
        prices = result.scalars().all()
        return [
            PriceAggregate(
                id=price.id,
                category=price.category,
                supplier=price.supplier,
                region=price.region,
                price_text=price.price_text,
            )
            for price in prices
        ], total

    async def create(
        self,
        category: str,
        supplier: str,
        region: str,
        price_text: str,
    ) -> PriceAggregate:
        """Создать новый прайс"""
        price = Price(
            category=category,
            supplier=supplier,
            region=region,
            price_text=price_text,
        )
        self.db.add(price)
        # Возвращаем агрегат без commit и refresh - commit делает uow
        # Для получения id нужно сделать flush
        await self.db.flush()
        return PriceAggregate(
            id=price.id,
            category=price.category,
            supplier=price.supplier,
            region=price.region,
            price_text=price.price_text,
        )

    async def update(
        self,
        price_id: int,
        category: Optional[str] = None,
        supplier: Optional[str] = None,
        region: Optional[str] = None,
        price_text: Optional[str] = None,
    ) -> PriceAggregate:
        """Обновить прайс"""
        values = {}
        if category is not None:
            values["category"] = category
        if supplier is not None:
            values["supplier"] = supplier
        if region is not None:
            values["region"] = region
        if price_text is not None:
            values["price_text"] = price_text

        query = (
            update(Price)
            .where(Price.id == price_id)
            .values(**values)
            .returning(Price)
        )
        result = await self.db.execute(query)
        price = result.scalar_one_or_none()
        if price:
            return PriceAggregate(
                id=price.id,
                category=price.category,
                supplier=price.supplier,
                region=price.region,
                price_text=price.price_text,
            )
        raise ValueError(f"Price with id {price_id} not found")

    async def delete(self, price_id: int) -> bool:
        """Удалить прайс по ID"""
        query = delete(Price).where(Price.id == price_id)
        result = await self.db.execute(query)
        return result.rowcount > 0
