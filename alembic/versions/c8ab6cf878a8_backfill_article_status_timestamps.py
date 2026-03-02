"""backfill_article_status_timestamps

Revision ID: c8ab6cf878a8
Revises: f4a7fa96e76e
Create Date: 2026-03-02 20:33:37.616494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8ab6cf878a8'
down_revision: Union[str, None] = 'f4a7fa96e76e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
            UPDATE articles
            SET approved_at = created_at
            WHERE status = 'APPROVED' AND approved_at IS NULL
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE articles
            SET archived_at = created_at
            WHERE status = 'ARCHIVED' AND archived_at IS NULL
            """
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
            UPDATE articles
            SET approved_at = NULL
            WHERE status = 'APPROVED' AND approved_at = created_at
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE articles
            SET archived_at = NULL
            WHERE status = 'ARCHIVED' AND archived_at = created_at
            """
        )
    )
