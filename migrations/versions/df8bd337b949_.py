"""empty message

Revision ID: df8bd337b949
Revises: 6069d0f045ca
Create Date: 2022-03-07 15:18:51.007768

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df8bd337b949'
down_revision = '6069d0f045ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'categories', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'categories', type_='foreignkey')
    op.drop_column('categories', 'user_id')
    # ### end Alembic commands ###