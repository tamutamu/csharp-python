"""Drop test

Revision ID: edc164933977
Revises: 277901684e5e
Create Date: 2023-03-25 09:11:53.258204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edc164933977'
down_revision = '277901684e5e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('backend_result', 'test')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('backend_result', sa.Column('test', sa.VARCHAR(), nullable=True))
    # ### end Alembic commands ###