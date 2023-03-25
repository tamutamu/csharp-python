"""Add test

Revision ID: 277901684e5e
Revises: bd33f9648aeb
Create Date: 2023-03-25 09:10:08.782158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '277901684e5e'
down_revision = 'bd33f9648aeb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('backend_result', sa.Column('test', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('backend_result', 'test')
    # ### end Alembic commands ###
