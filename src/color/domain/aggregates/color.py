from dataclasses import dataclass
from typing import Optional


@dataclass
class ColorAggregate:
    """Агрегат цвета"""
    name: str


@dataclass
class ColorAssignAggregate:
    """Агрегат назначения цвета"""
    id: int
    key: str
    color: str
