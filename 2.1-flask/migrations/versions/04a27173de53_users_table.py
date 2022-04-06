"""users table

Revision ID: 04a27173de53
Revises: 
Create Date: 2022-04-02 23:28:10.445282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04a27173de53'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('advertisement',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('owner', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('advertisement')
    # ### end Alembic commands ###