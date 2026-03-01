from sqlalchemy import BigInteger, Column, ForeignKey, String, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from src.core.db.database import Base
from src.core.db.mixins import TimestampMixin


class Color(TimestampMixin, Base):
    __tablename__ = "color"

    _name = Column(
        "name",
        String(50),
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
    assignments = relationship(
        "ColorAssign",
        back_populates="color_obj",
        cascade="all, delete-orphan",
    )


class ColorAssign(TimestampMixin, Base):
    __tablename__ = "color_assign"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    key = Column(
        String(50),
        nullable=False,
        index=True,
    )

    color = Column(
        String(50),
        ForeignKey("color.name", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Уникальное ограничение на сочетание key + color
    __table_args__ = (
        UniqueConstraint("key", "color", name="uq_color_assign_key_color"),
    )

    # Связь многие-к-одному
    color_obj = relationship(
        "Color",
        back_populates="assignments",
    )