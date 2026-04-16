"""add password reset fields to user

Revision ID: 5a8d1b2c3f4e
Revises: dbcc4ca70ffd_initial_scheme
Create Date: 2026-04-16 00:00:00.000000
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "5a8d1b2c3f4e"
down_revision = "dbcc4ca70ffd_initial_scheme"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("password_reset_token", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column(
            "password_reset_token_expired_at", sa.DateTime(timezone=True), nullable=True
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "password_reset_token_expired_at")
    op.drop_column("users", "password_reset_token")
