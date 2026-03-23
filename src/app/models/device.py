from sqlalchemy import Column, Enum, Integer, String, Table

from app.entities.device import DeviceType

from .base import metadata

devices = Table(
    "devices",
    metadata,
    # Identificador único del dispositivo en la base de datos
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("device_uuid", String(64), nullable=False, unique=True),
    Column("activation_code", String(100), nullable=False, unique=True),
    Column("type", Enum(DeviceType), nullable=False),
)
