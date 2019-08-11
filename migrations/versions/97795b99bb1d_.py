"""empty message

Revision ID: 97795b99bb1d
Revises: 2a3ceebcfeba
Create Date: 2019-08-11 12:20:22.979443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97795b99bb1d'
down_revision = '2a3ceebcfeba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('properties', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'properties', 'addresses', ['address_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'properties', type_='foreignkey')
    op.drop_column('properties', 'address_id')
    # ### end Alembic commands ###