"""rename subscribers table to emails

Revision ID: b6a4e1d9c8f2
Revises: 8a1d5f7c2b43
Create Date: 2026-09-04 00:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b6a4e1d9c8f2"
down_revision: str | Sequence[str] | None = "8a1d5f7c2b43"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table("subscribers", "emails")
    op.execute("ALTER INDEX ix_subscribers_id RENAME TO ix_emails_id")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER INDEX ix_emails_id RENAME TO ix_subscribers_id")
    op.rename_table("emails", "subscribers")
