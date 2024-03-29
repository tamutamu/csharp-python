"""from

Revision ID: e9a00a107207
Revises: 85579a728521
Create Date: 2023-03-27 19:29:22.619244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9a00a107207'
down_revision = '85579a728521'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('system_setting',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('value', sa.String(), nullable=True),
    sa.Column('created', sa.DATETIME(), nullable=False),
    sa.Column('modified', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.drop_table('setting')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('setting',
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('value', sa.VARCHAR(), nullable=True),
    sa.Column('created', sa.DATETIME(), nullable=False),
    sa.Column('modified', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.drop_table('system_setting')
    # ### end Alembic commands ###
