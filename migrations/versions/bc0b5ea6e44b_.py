"""empty message

Revision ID: bc0b5ea6e44b
Revises: 
Create Date: 2020-02-20 18:46:48.689709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc0b5ea6e44b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lender', sa.String(length=80), nullable=True),
    sa.Column('borrower', sa.String(length=255), nullable=True),
    sa.Column('amount', sa.Numeric(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    # ### end Alembic commands ###