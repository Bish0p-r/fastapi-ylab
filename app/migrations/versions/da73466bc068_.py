"""empty message

Revision ID: da73466bc068
Revises: 253cc43b42d1
Create Date: 2024-02-12 22:08:30.450508

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da73466bc068'
down_revision: str | None = '253cc43b42d1'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dishes', 'discount')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dishes', sa.Column('discount', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
