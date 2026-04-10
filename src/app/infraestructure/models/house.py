from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table

from .base import metadata

houses = Table(
    "houses",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(12), nullable=False),
    Column(
        "user_id",
        ForeignKey("users.id", name="fk_houses_user_id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("location", String(50), nullable=True),
    Column("invitation_validation", Boolean, nullable=False),
)
