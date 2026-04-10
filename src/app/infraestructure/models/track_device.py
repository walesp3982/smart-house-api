from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, Integer, Table

from app.entities.track_device import StatusDevice

from .base import metadata

track_devices = Table(
    "track_devices",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "device_id",
        ForeignKey(
            "installed_devices.id",
            name="fk_track_devices_device_id",
            ondelete="CASCADE",
        ),
        nullable=False,
    ),
    Column("status", Enum(StatusDevice), nullable=False),
    Column("timestamp", TIMESTAMP, nullable=False),
)
