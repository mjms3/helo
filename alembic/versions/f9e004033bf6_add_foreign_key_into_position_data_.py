"""Add foreign key into position_data table to helicopters table

Revision ID: f9e004033bf6
Revises: 44efa78647ce
Create Date: 2017-02-05 10:57:41.213227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9e004033bf6'
down_revision = '44efa78647ce'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('helicopters', sa.Column('position_data_Id', sa.Integer))


def downgrade():
    op.drop_column('helicopters','position_data_Id')
