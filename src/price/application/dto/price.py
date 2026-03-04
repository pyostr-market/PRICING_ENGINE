from dataclasses import dataclass
from typing import Optional


@dataclass
class CategoryDTO:
    """DTO для категории"""
    name: str


@dataclass
class SupplierDTO:
    """DTO для поставщика"""
    name: str


@dataclass
class RegionDTO:
    """DTO для региона"""
    name: str


@dataclass
class PriceDTO:
    """DTO для прайса"""
    id: Optional[int] = None
    category: Optional[str] = None
    supplier: Optional[str] = None
    region: Optional[str] = None
    price_text: Optional[str] = None


@dataclass
class PriceCreateDTO:
    """DTO для создания прайса"""
    category: str
    supplier: str
    region: str
    price_text: str


@dataclass
class PriceUpdateDTO:
    """DTO для обновления прайса"""
    category: Optional[str] = None
    supplier: Optional[str] = None
    region: Optional[str] = None
    price_text: Optional[str] = None
