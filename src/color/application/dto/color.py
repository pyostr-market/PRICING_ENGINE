from dataclasses import dataclass
from typing import Optional


@dataclass
class ColorDTO:
    """DTO для цвета"""
    name: str


@dataclass
class ColorAssignDTO:
    """DTO для назначения цвета"""
    id: Optional[int] = None
    key: Optional[str] = None
    color: Optional[str] = None


@dataclass
class ColorAssignCreateDTO:
    """DTO для создания назначения цвета"""
    key: str
    color: str


@dataclass
class ColorAssignUpdateDTO:
    """DTO для обновления назначения цвета"""
    key: Optional[str] = None
    color: Optional[str] = None
