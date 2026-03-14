from enum import StrEnum

from sqlalchemy import Column, Enum, Integer, String, Table

from .base import metadata


class AreaType(StrEnum):
    living_room = "living_room"
    bedroom = "bedroom"
    kitchen = "kitchen"
    outside = "outside"


areas = Table(
    "areas",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), nullable=False),
    Column("type", Enum(AreaType), nullable=False),
)
