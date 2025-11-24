"""Fix cascade nullable=False

Revision ID: c29118c14903
Revises: adf133cb7a1d
Create Date: 2025-11-23 17:43:38.067333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c29118c14903'
down_revision = 'adf133cb7a1d'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('chat_history', schema=None) as batch_op:

        batch_op.alter_column(
            'user_id',
            existing_type=sa.INTEGER(),
            nullable=False
        )

        # CRIAR FK com nome explícito
        batch_op.create_foreign_key(
            "fk_chat_history_user_id",   # <-- NOME DA FK (obrigatório)
            'user',
            ['user_id'],
            ['id'],
            ondelete='CASCADE'
        )


def downgrade():
    with op.batch_alter_table('chat_history', schema=None) as batch_op:

        # Remover a FK pelo nome
        batch_op.drop_constraint(
            "fk_chat_history_user_id",
            type_='foreignkey'
        )

        # Recriar FK antiga SEM CASCADE
        batch_op.create_foreign_key(
            "fk_chat_history_user_id",
            'user',
            ['user_id'],
            ['id']
        )

        batch_op.alter_column(
            'user_id',
            existing_type=sa.INTEGER(),
            nullable=True
        )
