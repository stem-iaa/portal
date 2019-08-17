"""empty message

Revision ID: 76e3d2749178
Revises: 8260c6171fa0
Create Date: 2019-08-16 19:20:30.410672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76e3d2749178'
down_revision = '8260c6171fa0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_solution_id', table_name='solution')
    op.drop_index('ix_solution_name', table_name='solution')
    op.drop_table('solution')
    op.drop_index('ix_file_id', table_name='file')
    op.drop_index('ix_file_path', table_name='file')
    op.drop_table('file')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('path', sa.VARCHAR(length=128), nullable=True),
    sa.Column('name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('solution_id', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_file_path', 'file', ['path'], unique=False)
    op.create_index('ix_file_id', 'file', ['id'], unique=False)
    op.create_table('solution',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('notes', sa.VARCHAR(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_solution_name', 'solution', ['name'], unique=False)
    op.create_index('ix_solution_id', 'solution', ['id'], unique=False)
    # ### end Alembic commands ###