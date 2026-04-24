"""merge chip_id y password reset

Revision ID: 9d15ba2f6b90
Revises: b6d1ff571bea, fbcaa71c6688
Create Date: 2026-04-21 14:12:33.480682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d15ba2f6b90'
down_revision: Union[str, Sequence[str], None] = ('b6d1ff571bea', 'fbcaa71c6688')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
