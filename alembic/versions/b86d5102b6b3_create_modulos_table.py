"""Create modulos table

Revision ID: b86d5102b6b3
Revises: 0255c251d5a9
Create Date: 2025-06-05 09:39:35.095757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b86d5102b6b3'
down_revision: Union[str, None] = '0255c251d5a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
