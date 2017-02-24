"""empty message

Revision ID: 0ee5ab7c3e54
Revises: 
Create Date: 2017-02-24 09:12:10.349183

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0ee5ab7c3e54'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('raw_data',
                    sa.Column('raw_data_id', sa.Integer(), nullable=False),
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('Icao', sa.Text(), nullable=True),
                    sa.Column('Reg', sa.Text(), nullable=True),
                    sa.Column('Alt', sa.Integer(), nullable=True),
                    sa.Column('GAlt', sa.Integer(), nullable=True),
                    sa.Column('Call', sa.Text(), nullable=True),
                    sa.Column('CallSus', sa.Boolean(), nullable=True),
                    sa.Column('Lat', sa.Numeric(precision=9, scale=6), nullable=True),
                    sa.Column('Long', sa.Numeric(precision=9, scale=6), nullable=True),
                    sa.Column('Spd', sa.Numeric(precision=5, scale=1), nullable=True),
                    sa.Column('Trak', sa.Numeric(precision=9, scale=6), nullable=True),
                    sa.Column('Type', sa.Text(), nullable=True),
                    sa.Column('Mdl', sa.Text(), nullable=True),
                    sa.Column('Man', sa.Text(), nullable=True),
                    sa.Column('CNum', sa.Text(), nullable=True),
                    sa.Column('From', sa.Text(), nullable=True),
                    sa.Column('To', sa.Text(), nullable=True),
                    sa.Column('Op', sa.String(191), nullable=True),
                    sa.Column('OpCode', sa.Text(), nullable=True),
                    sa.Column('Mil', sa.Boolean(), nullable=True),
                    sa.Column('Cou', sa.Text(), nullable=True),
                    sa.Column('Gnd', sa.Boolean(), nullable=True),
                    sa.Column('TimeStamp', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('raw_data_id')
                    )

    op.create_unique_constraint('uq_raw_data', 'raw_data', ['Id', 'TimeStamp'])


def downgrade():
    op.drop_table('raw_data')
