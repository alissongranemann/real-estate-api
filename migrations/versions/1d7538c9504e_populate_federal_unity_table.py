# flake8: noqa
"""populate federal unity table

Revision ID: 1d7538c9504e
Revises: 5892a034b273
Create Date: 2019-12-15 14:33:14.607142

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "1d7538c9504e"
down_revision = "5892a034b273"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Acre', 'AC');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Alagoas', 'AL');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Amapá', 'AP');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Amazonas', 'AM');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Bahia', 'BA');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Ceará', 'CE');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Espírito Santo', 'ES');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Goiás', 'GO');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Maranhão', 'MA');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Mato Grosso', 'MT');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Mato Grosso do Sul', 'MS');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Minas Gerais', 'MG');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Pará', 'PA');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Paraíba', 'PB');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Paraná', 'PR');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Pernambuco', 'PE');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Piauí', 'PI');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Rio de Janeiro', 'RJ');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Rio Grande do Norte', 'RN');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Rio Grande do Sul', 'RS');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Rondônia', 'RO');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Roraima', 'RR');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Santa Catarina', 'SC');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'São Paulo', 'SP');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Sergipe', 'SE');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Tocantins', 'TO');"
    )
    op.execute(
        "INSERT INTO federal_unity (id, name, short_name) VALUES (nextval('federal_unity_id_seq'), 'Distrito Federal', 'DF');"
    )


def downgrade():
    op.execute("DELETE FROM federal_unity;")
