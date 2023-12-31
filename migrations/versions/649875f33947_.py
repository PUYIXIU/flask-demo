"""empty message

Revision ID: 649875f33947
Revises: b8ac07a4c612
Create Date: 2023-10-18 17:14:51.129068

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '649875f33947'
down_revision = 'b8ac07a4c612'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=200), nullable=False))
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', mysql.VARCHAR(length=200), nullable=False))
        batch_op.drop_column('username')

    # ### end Alembic commands ###
