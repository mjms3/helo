"""empty message

Revision ID: 312d95bb3c45
Revises: 0ee5ab7c3e54
Create Date: 2017-02-24 10:33:11.679163

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '312d95bb3c45'
down_revision = '0ee5ab7c3e54'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('canonical_operators',
                    sa.Column('canonical_operator_id', sa.Integer(), nullable=False),
                    sa.Column('canonical_operator_name', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('canonical_operator_id'),
                    )
    op.create_table('routes',
                    sa.Column('route_id', sa.Integer(), nullable=False),
                    sa.Column('elapsed_time_min', sa.Integer(), nullable=False),
                    sa.Column('distance_travelled', sa.Numeric(precision=18, scale=8), nullable=False),
                    sa.PrimaryKeyConstraint('route_id'),
                    )
    op.create_table('operators',
                    sa.Column('operator_id', sa.Integer(), nullable=False),
                    sa.Column('operator_name', sa.String(191), nullable=True),
                    sa.Column('is_military', sa.Boolean(), nullable=True),
                    sa.Column('canonical_operator_id', sa.Integer(), nullable=True),
                    sa.Column('operator_country', sa.Text(), nullable=True),
                    sa.ForeignKeyConstraint(['canonical_operator_id'], ['canonical_operators.canonical_operator_id'], ),
                    sa.PrimaryKeyConstraint('operator_id'),
                    sa.UniqueConstraint('operator_name')
                    )
    op.create_table('helicopters',
                    sa.Column('helicopter_id', sa.Integer(), nullable=False),
                    sa.Column('helicopter_data_source_id', sa.Integer(), nullable=False),
                    sa.Column('icao', sa.String(6), nullable=False),
                    sa.Column('registration', sa.String(10), nullable=False),
                    sa.Column('helicopter_type', sa.Text(), nullable=False),
                    sa.Column('helicopter_model', sa.Text(), nullable=False),
                    sa.Column('helicopter_operator_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['helicopter_operator_id'], ['operators.operator_id'], ),
                    sa.PrimaryKeyConstraint('helicopter_id'),
                    sa.UniqueConstraint('helicopter_data_source_id'),
                    sa.UniqueConstraint('icao'),
                    sa.UniqueConstraint('registration'),
                    )
    op.create_table('position_readings',
                    sa.Column('position_reading_id', sa.Integer(), nullable=False),
                    sa.Column('helicopter_id', sa.Integer(), nullable=False),
                    sa.Column('latitude', sa.Numeric(precision=9, scale=6), nullable=False),
                    sa.Column('longitude', sa.Numeric(precision=9, scale=6), nullable=False),
                    sa.Column('altitude', sa.Integer(), nullable=True),
                    sa.Column('barometric_altitude', sa.Integer(), nullable=True),
                    sa.Column('speed', sa.Numeric(precision=5, scale=1), nullable=True),
                    sa.Column('bearing', sa.Numeric(precision=9, scale=6), nullable=True),
                    sa.Column('minutes_since_last_reading', sa.Integer(), nullable=True),
                    sa.Column('knots_moved_since_last_reading', sa.Numeric(precision=18, scale=8), nullable=True),
                    sa.Column('calculated_speed', sa.Numeric(precision=18, scale=8), nullable=True),
                    sa.Column('route_id', sa.Integer(), nullable=True),
                    sa.Column('time_stamp', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['helicopter_id'], ['helicopters.helicopter_id'], ),
                    sa.ForeignKeyConstraint(['route_id'], ['routes.route_id'], ),
                    sa.PrimaryKeyConstraint('position_reading_id')
                    )

    op.create_unique_constraint('uq_position_reading_heli_time', 'position_readings', ['helicopter_id', 'time_stamp'])


def downgrade():
    op.drop_table('position_readings')
    op.drop_table('helicopters')
    op.drop_table('operators')
    op.drop_table('routes')
    op.drop_table('canonical_operators')
