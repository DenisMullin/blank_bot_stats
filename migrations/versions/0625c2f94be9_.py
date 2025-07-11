"""empty message

Revision ID: 0625c2f94be9
Revises: f0e77d7e1deb
Create Date: 2025-06-30 02:35:07.609583

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0625c2f94be9'
down_revision: Union[str, None] = 'f0e77d7e1deb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('sbp_pressed', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('state', sa.String(length=255), nullable=True))
    op.drop_column('user', 'button_pressed_10')
    op.drop_column('user', 'button_pressed_5')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('button_pressed_5', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('button_pressed_10', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('user', 'state')
    op.drop_column('user', 'sbp_pressed')
    # ### end Alembic commands ###
