"""Add operators and helicopters tables

Revision ID: 88c5e282013b
Revises: f6670965a752
Create Date: 2017-02-04 14:21:58.657743

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '88c5e282013b'
down_revision = 'f6670965a752'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('operators',
                    sa.Column('operator_id', sa.Integer, primary_key=True),
                    sa.Column('canonical_operator_name', sa.Text),
                    )

    op.add_column('position_data',
                  sa.Column('operator_id', sa.Integer, sa.ForeignKey('operators.operator_id', name='fk_position_data_operator_id'))
                  )

    op.create_table('helicopters',
                    sa.Column('helicopter_id', sa.Integer, primary_key=True),
                    sa.Column('helicopter_reg', sa.Text),
                    sa.Column('operator_id', sa.Integer, sa.ForeignKey('operators.operator_id', name='fk_helicopters_operator_id')),
                    )


def downgrade():
    op.drop_table('helicopters')
    op.drop_constraint('fk_position_data_operator_id','position_data',type_='foreignkey')
    op.drop_column('position_data','operator_id')
    op.drop_table('operators')
