"""empty message

Revision ID: c50fdbbcfb6a
Revises: 
Create Date: 2024-06-03 18:43:41.222816

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c50fdbbcfb6a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lotteries', sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='作成日時'))
    op.add_column('lotteries', sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=True, comment='更新日時'))
    op.alter_column('lotteries', 'text',
               existing_type=sa.TEXT(),
               type_=sa.VARCHAR(length=4096),
               existing_nullable=False)
    op.alter_column('lotteries', 'title',
               existing_type=sa.TEXT(),
               type_=sa.VARCHAR(length=256),
               existing_nullable=False)
    op.add_column('users', sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='作成日時'))
    op.add_column('users', sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=True, comment='更新日時'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
    op.alter_column('lotteries', 'title',
               existing_type=sa.VARCHAR(length=256),
               type_=sa.TEXT(),
               existing_nullable=False)
    op.alter_column('lotteries', 'text',
               existing_type=sa.VARCHAR(length=4096),
               type_=sa.TEXT(),
               existing_nullable=False)
    op.drop_column('lotteries', 'updated_at')
    op.drop_column('lotteries', 'created_at')
    # ### end Alembic commands ###
