from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table

from .base import metadata

houses = Table(
    "houses",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("local_id", String(45), nullable=False),
    Column("name", String(12), nullable=False),
    Column("user_id", ForeignKey("users.id", name="fk_houses_user_id"), nullable=False),
    Column("location", String(50), nullable=True),
    Column("invitation_validation", Boolean, nullable=False),
)
