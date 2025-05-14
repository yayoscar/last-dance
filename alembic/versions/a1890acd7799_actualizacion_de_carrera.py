"""Actualizacion de Carrera

Revision ID: a1890acd7799
Revises: 3a1c5641f8d4
Create Date: 2025-05-12 07:30:40.307619

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1890acd7799'
down_revision: Union[str, None] = '3a1c5641f8d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
