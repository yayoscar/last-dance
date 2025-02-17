"""cambio de curp a 18 caracteres

Revision ID: dd245c235d81
Revises: 0722e62425aa
Create Date: 2025-02-17 08:04:30.735877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd245c235d81'
down_revision: Union[str, None] = '0722e62425aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
