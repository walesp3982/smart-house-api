from enum import StrEnum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Table

from .base import metadata


class DeviceType(StrEnum):
    LIGHT = "light"
    THERMOSTAT = "thermostat"
    CAMERA = "camera"
    LOCK = "lock"
    SENSOR = "sensor"


devices = Table(
    "devices",
    metadata,
    # Identificador único del dispositivo en la base de datos
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), nullable=False),
    Column("house_id", ForeignKey("houses.id"), nullable=False),
    # Identificador del dispositivo en el hardware
    Column("device_uuid", String(64), nullable=False),
    Column("area_id", ForeignKey("areas.id"), nullable=True),
    Column("type", Enum(DeviceType), nullable=False),
)
