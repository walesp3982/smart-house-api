from sqlalchemy import Column, ForeignKey, Integer, String, Table

from .base import metadata

installed_devices = Table(
    "installed_devices",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), nullable=False),
    Column(
        "device_id",
        ForeignKey(
            "devices.id",
            ondelete="CASCADE",
            name="fk_device",
        ),
        nullable=False,
    ),
    Column(
        "house_id",
        ForeignKey(
            "houses.id",
            ondelete="SET NULL",
            name="fk_house",
        ),
        nullable=True,
    ),
    Column(
        "user_id",
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
            name="fk_user",
        ),
        nullable=False,
    ),
    Column(
        "area_id",
        ForeignKey(
            "areas.id",
            ondelete="SET NULL",
            name="fk_areas",
        ),
        nullable=True,
    ),
)
