"""modificações do henriquoso

Revision ID: b8c41a19ebff
Revises: e4cfbfd0ab4c
Create Date: 2025-01-03 14:00:56.198828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8c41a19ebff'
down_revision = 'e4cfbfd0ab4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('template_question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('risk_level', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('template_question', schema=None) as batch_op:
        batch_op.drop_column('risk_level')

    # ### end Alembic commands ###
