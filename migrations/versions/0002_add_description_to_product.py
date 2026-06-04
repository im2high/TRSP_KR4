"""add description to product (NOT NULL)

Revision ID: 0002
Revises: 0001
Create Date: 2025-01-01 00:10:00
"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1) Добавляем колонку с server_default, чтобы существующие строки
    #    получили значение и не нарушили ограничение NOT NULL.
    with op.batch_alter_table("product") as batch_op:
        batch_op.add_column(
            sa.Column(
                "description",
                sa.String(length=1000),
                nullable=False,
                server_default="",
            )
        )
    # 2) Снимаем server_default — дальше description должен задаваться явно.
    with op.batch_alter_table("product") as batch_op:
        batch_op.alter_column("description", server_default=None)


def downgrade() -> None:
    with op.batch_alter_table("product") as batch_op:
        batch_op.drop_column("description")
