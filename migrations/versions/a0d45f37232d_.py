"""empty message

Revision ID: a0d45f37232d
Revises: a3317e14117c
Create Date: 2023-01-10 10:43:40.671109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0d45f37232d'
down_revision = 'a3317e14117c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password_hash', sa.String(length=100), nullable=False))
    op.add_column('user', sa.Column('address', sa.String(length=100), nullable=False))
    op.drop_column('user', 'password')
    op.drop_column('user', 'adress')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('adress', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('password', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.drop_column('user', 'address')
    op.drop_column('user', 'password_hash')
    # ### end Alembic commands ###
