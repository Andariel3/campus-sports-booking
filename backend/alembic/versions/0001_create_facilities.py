"""create facilities table

Revision ID: 0001
Revises:
Create Date: 2026-11-11

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

sport_type = sa.Enum(
    "football", "basketball", "tennis", "volleyball", "handball", "swimming", name="sport_type"
)


def upgrade() -> None:
    op.create_table(
        "facilities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True),
        sa.Column("sport", sport_type, nullable=False),
        sa.Column("location", sa.String(length=200), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
    )


def downgrade() -> None:
    op.drop_table("facilities")
    sport_type.drop(op.get_bind(), checkfirst=True)
