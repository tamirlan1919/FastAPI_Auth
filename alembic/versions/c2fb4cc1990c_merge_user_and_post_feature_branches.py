"""Merge user and post feature branches

Revision ID: c2fb4cc1990c
Revises: efc17b817199
Create Date: 2026-10-13 21:19:29.572736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2fb4cc1990c'
down_revision: Union[str, Sequence[str], None] = 'efc17b817199'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
