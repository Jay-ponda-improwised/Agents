"""create chat history and models tables

Revision ID: 4f9973f7f7f0
Revises: None
Create Date: 2025-12-01 10:25:08.588444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f9973f7f7f0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'models',
        sa.Column('id', sa.UUID(), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('model_name', sa.String(), nullable=False, unique=True),
    )
    op.create_table(
        'chat_history',
        sa.Column('id', sa.UUID(), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('params', sa.JSON(), nullable=True),
        sa.Column('model_id', sa.UUID(), sa.ForeignKey('models.id'), nullable=False),
        sa.Column('parent_id', sa.UUID(), sa.ForeignKey('chat_history.id'), nullable=True),
        sa.Column('request_route', sa.String(), nullable=False),
        sa.Column('answers', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('archived_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('chat_history')
    op.drop_table('models')