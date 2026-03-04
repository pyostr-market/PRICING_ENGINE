from sqlalchemy import BigInteger, Column, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from src.core.db.database import Base
from src.core.db.mixins import TimestampMixin


class Category(TimestampMixin, Base):
    __tablename__ = "category"

    _name = Column(
        "name",
        String(100),
        primary_key=True,
        nullable=False,
        unique=True,
        index=True,
    )

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value.lower() if value else None

    # Связь один-ко-многим
    prices = relationship(
        "Price",
        back_populates="category_obj",
        cascade="all, delete-orphan",
    )


class Supplier(TimestampMixin, Base):
    __tablename__ = "supplier"

    _name = Column(
        "name",
        String(200),
        primary_key=True,
        nullable=False,
        unique=True,
        index=True,
    )

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value.lower() if value else None

    # Связь один-ко-многим
    prices = relationship(
        "Price",
        back_populates="supplier_obj",
        cascade="all, delete-orphan",
    )


class Region(TimestampMixin, Base):
    __tablename__ = "region"

    _name = Column(
        "name",
        String(100),
        primary_key=True,
        nullable=False,
        unique=True,
        index=True,
    )

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value.lower() if value else None

    # Связь один-ко-многим
    prices = relationship(
        "Price",
        back_populates="region_obj",
        cascade="all, delete-orphan",
    )


class Price(TimestampMixin, Base):
    __tablename__ = "price"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    category = Column(
        String(100),
        ForeignKey("category.name", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    supplier = Column(
        String(200),
        ForeignKey("supplier.name", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    region = Column(
        String(100),
        ForeignKey("region.name", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    price_text = Column(
        Text,
        nullable=False,
    )

    # Уникальное ограничение на сочетание category + supplier + region
    __table_args__ = (
        UniqueConstraint("category", "supplier", "region", name="uq_price_category_supplier_region"),
    )

    # Связи многие-к-одному
    category_obj = relationship(
        "Category",
        back_populates="prices",
    )

    supplier_obj = relationship(
        "Supplier",
        back_populates="prices",
    )

    region_obj = relationship(
        "Region",
        back_populates="prices",
    )
