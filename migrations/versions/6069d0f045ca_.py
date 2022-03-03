"""empty message

Revision ID: 6069d0f045ca
Revises: 
Create Date: 2022-03-03 11:56:44.344268

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '6069d0f045ca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.Column('created', sa.DateTime(), nullable=False),
                    sa.Column('updated', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sqlalchemy_utils.types.email.EmailType(
                        length=255), nullable=False),
                    sa.Column('password_hash', sa.String(length=64), nullable=False),
                    sa.Column('salt', sa.String(length=12), nullable=False),
                    sa.Column('created', sa.DateTime(), nullable=False),
                    sa.Column('updated', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('items',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=80), nullable=False),
                    sa.Column('description', sa.String(length=200), nullable=True),
                    sa.Column('created', sa.DateTime(), nullable=False),
                    sa.Column('updated', sa.DateTime(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('category_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_items_name'), 'items', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_items_name'), table_name='items')
    op.drop_table('items')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('categories')
    # ### end Alembic commands ###