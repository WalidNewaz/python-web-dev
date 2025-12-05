"""Add users model

Revision ID: bb817b3c290b
Revises: 080dc787cbd9
Create Date: 2025-12-05 03:03:27.027339

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb817b3c290b'
down_revision: Union[str, Sequence[str], None] = '080dc787cbd9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
