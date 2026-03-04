from dataclasses import dataclass
from typing import Optional


@dataclass
class CategoryAggregate:
    """Агрегат категории"""
    name: str


@dataclass
class SupplierAggregate:
    """Агрегат поставщика"""
    name: str


@dataclass
class RegionAggregate:
    """Агрегат региона"""
    name: str


@dataclass
class PriceAggregate:
    """Агрегат прайса"""
    id: int
    category: str
    supplier: str
    region: str
    price_text: str
