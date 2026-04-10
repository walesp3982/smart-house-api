from sqlalchemy import Boolean, Column, DateTime, Integer, String, Table

from .base import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), nullable=False),
    Column("email", String(50), unique=True, nullable=False),
    Column("password", String(128), nullable=False),
    Column("is_verified", Boolean, nullable=False),
    Column("verification_token", String(100), nullable=True),
    Column("verification_token_expired_at", DateTime(timezone=True), nullable=True),
)
