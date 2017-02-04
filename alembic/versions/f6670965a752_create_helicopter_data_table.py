"""Create helicopter data table

Revision ID: f6670965a752
Revises: 
Create Date: 2017-01-28 16:44:29.095265

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f6670965a752'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('position_data',
                    sa.Column('position_data_id', sa.Integer, primary_key=True),
                    sa.Column('Id', sa.Integer),
                    sa.Column('Icao', sa.Text),
                    sa.Column('Reg', sa.Text),
                    sa.Column('Alt', sa.Integer),
                    sa.Column('GAlt', sa.Integer),
                    sa.Column('Call', sa.Text),
                    sa.Column('CallSus', sa.Boolean),
                    sa.Column('Lat', sa.Numeric(precision=9, scale=6)),
                    sa.Column('Long', sa.Numeric(precision=9, scale=6)),
                    sa.Column('Spd', sa.Numeric(precision=5, scale=1)),
                    sa.Column('Trak', sa.Numeric(precision=9, scale=6)),
                    sa.Column('Type', sa.Text),
                    sa.Column('Mdl', sa.Text),
                    sa.Column('Man', sa.Text),
                    sa.Column('CNum', sa.Text),
                    sa.Column('From', sa.Text),
                    sa.Column('To', sa.Text),
                    sa.Column('Op', sa.Text),
                    sa.Column('OpCode', sa.Text),
                    sa.Column('Mil', sa.Boolean),
                    sa.Column('Cou', sa.Text),
                    sa.Column('Gnd', sa.Boolean),
                    sa.Column('TimeStamp', sa.DateTime)
                    )

    op.create_unique_constraint('uq_position_data', 'position_data', ['Id', 'TimeStamp'])

def downgrade():
    op.drop_table('position_data')
