"""empty message

Revision ID: 2a3ceebcfeba
Revises: daad7fb14035
Create Date: 2019-08-11 12:14:50.512160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2a3ceebcfeba"
down_revision = "daad7fb14035"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "addresses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("neighbourhood", sa.String(), nullable=True),
        sa.Column("cep", sa.String(length=9), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_column("properties", "neighbourhood")
    op.drop_column("properties", "city")
    op.drop_column("properties", "cep")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "properties",
        sa.Column("cep", sa.VARCHAR(length=9), autoincrement=False, nullable=True),
    )
    op.add_column(
        "properties",
        sa.Column("city", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "properties",
        sa.Column("neighbourhood", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_table("addresses")
    # ### end Alembic commands ###
