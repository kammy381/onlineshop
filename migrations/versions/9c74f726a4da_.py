"""empty message

Revision ID: 9c74f726a4da
Revises: 
Create Date: 2023-01-03 19:08:15.643945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c74f726a4da'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('merchant_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    # ### end Alembic commands ###
