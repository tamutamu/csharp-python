"""Add setting

Revision ID: 85579a728521
Revises: 4667cfa90013
Create Date: 2023-03-26 23:50:32.765257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85579a728521'
down_revision = '4667cfa90013'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('setting',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('value', sa.String(), nullable=True),
    sa.Column('created', sa.DATETIME(), nullable=False),
    sa.Column('modified', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.drop_column('backend_result', 'hoge')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('backend_result', sa.Column('hoge', sa.VARCHAR(), nullable=True))
    op.drop_table('setting')
    # ### end Alembic commands ###
