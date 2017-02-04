"""Add table for routes data

Revision ID: 44efa78647ce
Revises: 88c5e282013b
Create Date: 2017-02-04 16:22:14.468056

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '44efa78647ce'
down_revision = '88c5e282013b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('routes',
                    sa.Column('route_id', sa.Integer, primary_key=True),
                    sa.Column('route_start_lat', sa.Numeric(precision=9, scale=6)),
                    sa.Column('route_start_long', sa.Numeric(precision=9, scale=6)),
                    sa.Column('route_end_lat', sa.Numeric(precision=9, scale=6)),
                    sa.Column('route_end_long', sa.Numeric(precision=9, scale=6)),
                    sa.Column('helicopter_id', sa.Integer, sa.ForeignKey('helicopters.helicopter_id', name='fk_routes_helicopter_id')),
                    )

    op.create_table('position_data_routes_rel',
                    sa.Column('position_data_routes_rel_id', sa.Integer, primary_key=True),
                    sa.Column('route_id', sa.Integer, sa.ForeignKey('routes.route_id',
                                                                    name='fk_pdr_rel_route_id')),
                    sa.Column('position_data_id', sa.Integer, sa.ForeignKey('position_data.position_data_id',
                                                                            name='fk_pdr_rel_position_data_id')),
                    )


def downgrade():
    op.drop_constraint('fk_routes_helicopter_id', 'routes', type_='foreignkey')
    op.drop_constraint('fk_pdr_rel_position_data_id', 'position_data_routes_rel', type_='foreignkey')
    op.drop_constraint('fk_pdr_rel_route_id', 'position_data_routes_rel', type_='foreignkey')

    op.drop_table('routes')
    op.drop_table('position_data_routes_rel')
