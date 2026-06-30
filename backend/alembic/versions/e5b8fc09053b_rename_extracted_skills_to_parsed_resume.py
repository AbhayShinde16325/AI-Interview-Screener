"""rename extracted_skills to parsed_resume

Revision ID: e5b8fc09053b
Revises: d411eb9c7f21
Create Date: 2026-06-28 19:30:31.589489

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e5b8fc09053b"
down_revision: Union[str, Sequence[str], None] = "d411eb9c7f21"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Rename extracted_skills -> parsed_resume"""

    op.alter_column(
        "resumes",
        "extracted_skills",
        new_column_name="parsed_resume",
    )


def downgrade() -> None:
    """Rename parsed_resume -> extracted_skills"""

    op.alter_column(
        "resumes",
        "parsed_resume",
        new_column_name="extracted_skills",
    )