"""empty message

Revision ID: ee87e51aace2
Revises: 41f77528f654
Create Date: 2025-06-29 19:50:40.295545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee87e51aace2'
down_revision: Union[str, None] = '41f77528f654'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('button_pressed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'button_pressed')
    # ### end Alembic commands ###
