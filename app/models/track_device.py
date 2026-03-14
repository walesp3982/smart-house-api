from enum import StrEnum

from sqlalchemy import TIMESTAMP, Column, Enum, Integer, String, Table

from .base import metadata


class StatusDevice(StrEnum):
    ON = "on"
    OFF = "off"


track_devices = Table(
    "track_devices",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("device_id", String(64), nullable=False),
    Column("status", Enum(StatusDevice), nullable=False),
    Column("timestamp", TIMESTAMP, nullable=False),
)
