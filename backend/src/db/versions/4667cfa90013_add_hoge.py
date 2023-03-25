"""Add hoge

Revision ID: 4667cfa90013
Revises: edc164933977
Create Date: 2023-03-25 09:12:40.920748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4667cfa90013'
down_revision = 'edc164933977'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('backend_result', sa.Column('hoge', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('backend_result', 'hoge')
    # ### end Alembic commands ###
