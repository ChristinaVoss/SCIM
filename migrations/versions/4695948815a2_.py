"""empty message

Revision ID: 4695948815a2
Revises: 
Create Date: 2021-05-27 16:45:07.026458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4695948815a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clubs', sa.Column('published', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('clubs', 'published')
    # ### end Alembic commands ###