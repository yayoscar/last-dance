"""update alumnos

Revision ID: 47ad22cc1c65
Revises: dd245c235d81
Create Date: 2025-02-18 22:24:34.767849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47ad22cc1c65'
down_revision: Union[str, None] = 'dd245c235d81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
