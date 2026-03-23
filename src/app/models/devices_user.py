from sqlalchemy import Column, ForeignKey, Integer, String, Table

from .base import metadata

devices_user = Table(
    "devices_user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("device_id", ForeignKey("devices.id"), nullable=False),
    Column("house_id", ForeignKey("houses.id"), nullable=False),
    Column("area_id", ForeignKey("areas.id"), nullable=True),
)
