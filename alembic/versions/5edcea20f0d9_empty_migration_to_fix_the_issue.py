"""Empty migration to fix the issue

Revision ID: 5edcea20f0d9
Revises: 724eb5d5a66a
Create Date: 2025-09-18 22:54:14.293888

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5edcea20f0d9'
down_revision: Union[str, Sequence[str], None] = '724eb5d5a66a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
