from enum import StrEnum

from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, Integer, Table

from .base import metadata


class StatusDevice(StrEnum):
    ON = "on"
    OFF = "off"


track_devices = Table(
    "track_devices",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "device_id",
        ForeignKey("devices.id", name="fk_track_devices_device_id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("status", Enum(StatusDevice), nullable=False),
    Column("timestamp", TIMESTAMP, nullable=False),
)
