from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint,
)

from app.entities.areas import AreaType

from .base import metadata

areas = Table(
    "areas",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), nullable=False),
    Column("type", Enum(AreaType), nullable=False),
    Column(
        "house_id",
        ForeignKey("houses.id", ondelete="CASCADE", name="fk_house"),
        nullable=False,
    ),
    UniqueConstraint("name", "house_id", name="name_unique_by_house_id"),
)
