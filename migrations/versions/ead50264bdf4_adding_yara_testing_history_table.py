"""adding yara_testing_history table

Revision ID: ead50264bdf4
Revises: 3a2003939cc4
Create Date: 2017-08-17 22:47:30.498042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ead50264bdf4'
down_revision = '3a2003939cc4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('yara_testing_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('yara_rule_id', sa.Integer(), nullable=False),
    sa.Column('revision', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
    sa.Column('end_time', sa.DateTime(timezone=True), nullable=False),
    sa.Column('files_tested', sa.Integer(), nullable=False),
    sa.Column('files_matched', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['kb_users.id'], ),
    sa.ForeignKeyConstraint(['yara_rule_id'], ['yara_rules.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('yara_testing_history')
    # ### end Alembic commands ###