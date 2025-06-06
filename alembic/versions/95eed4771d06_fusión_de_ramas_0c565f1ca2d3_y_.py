"""Fusión de ramas 0c565f1ca2d3 y a21d4fe6970e

Revision ID: 95eed4771d06
Revises: 0c565f1ca2d3, a21d4fe6970e
Create Date: 2025-06-06 09:19:36.182032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95eed4771d06'
down_revision: Union[str, None] = ('0c565f1ca2d3', 'a21d4fe6970e')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
