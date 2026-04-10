from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, Table

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
            name="fk_device_in_installed_device",
        ),
        nullable=False,
    ),
    Column(
        "house_id",
        ForeignKey(
            "houses.id",
            ondelete="RESTRICT",
            name="fk_house_in_installed_device",
        ),
        nullable=True,
    ),
    Column(
        "user_id",
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
            name="fk_user_in_installed_device",
        ),
        nullable=False,
    ),
    Column(
        "area_id",
        ForeignKey(
            "areas.id",
            ondelete="RESTRICT",
            name="fk_areas_in_installed_device",
        ),
        nullable=True,
    ),
    CheckConstraint(
        "area_id IS NULL OR house_id IS NOT NULL",
        name="chkk_area_requires_house",
    ),
)
