"""replace old interview schema

Revision ID: 9c0a9747acca
Revises: e5b8fc09053b
Create Date: 2026-06-30 17:38:21.945135

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9c0a9747acca'
down_revision: Union[str, Sequence[str], None] = 'e5b8fc09053b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Replace the old interview schema with the new one."""
    op.create_table(
        'interviews',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'interview_questions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('interview_id', sa.UUID(), nullable=False),
        sa.Column('question_order', sa.Integer(), nullable=False),
        sa.Column('skill', sa.String(), nullable=False),
        sa.Column('difficulty', sa.String(), nullable=False),
        sa.Column('question_type', sa.String(), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column(
            'expected_topics',
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column('knowledge_source', sa.String(), nullable=False),
        sa.Column('candidate_answer', sa.Text(), nullable=True),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['interview_id'], ['interviews.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    # Drop the old tables (answers → questions → summaries → sessions)
    op.drop_index(op.f("ix_answers_question_id"), table_name="answers")
    op.drop_table("answers")

    op.drop_index(op.f("ix_questions_interview_session_id"), table_name="questions")
    op.drop_table("questions")

    op.drop_index(
        op.f("ix_interview_summaries_interview_session_id"),
        table_name="interview_summaries",
    )
    op.drop_table("interview_summaries")

    op.drop_index(op.f("ix_interview_sessions_resume_id"), table_name="interview_sessions")
    op.drop_index(op.f("ix_interview_sessions_user_id"), table_name="interview_sessions")
    op.drop_table("interview_sessions")


def downgrade() -> None:
    """Restore the old interview schema."""
    op.create_table(
        'questions',
        sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('interview_session_id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('question_number', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('question_text', sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column('difficulty', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
        sa.Column('source', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
        sa.Column('context_snapshot', sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['interview_session_id'],
            ['interview_sessions.id'],
            name=op.f('questions_interview_session_id_fkey'),
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('questions_pkey')),
    )
    op.create_index(
        op.f('ix_questions_interview_session_id'),
        'questions',
        ['interview_session_id'],
        unique=False,
    )

    op.create_table(
        'interview_sessions',
        sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('resume_id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('role', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.Column('status', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
        sa.Column('question_count', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('current_question', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('knowledge_base_version', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
        sa.Column(
            'started_at',
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column('completed_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['resume_id'],
            ['resumes.id'],
            name=op.f('interview_sessions_resume_id_fkey'),
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            name=op.f('interview_sessions_user_id_fkey'),
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('interview_sessions_pkey')),
    )
    op.create_index(op.f('ix_interview_sessions_user_id'), 'interview_sessions', ['user_id'], unique=False)
    op.create_index(op.f('ix_interview_sessions_resume_id'), 'interview_sessions', ['resume_id'], unique=False)

    op.create_table(
        'interview_summaries',
        sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('interview_session_id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('overall_score', sa.NUMERIC(precision=5, scale=2), autoincrement=False, nullable=False),
        sa.Column('technical_score', sa.NUMERIC(precision=5, scale=2), autoincrement=False, nullable=False),
        sa.Column('communication_score', sa.NUMERIC(precision=5, scale=2), autoincrement=False, nullable=False),
        sa.Column(
            'strengths',
            postgresql.JSONB(astext_type=sa.Text()),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            'improvements',
            postgresql.JSONB(astext_type=sa.Text()),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column('final_feedback', sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column('recommendation', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['interview_session_id'],
            ['interview_sessions.id'],
            name=op.f('interview_summaries_interview_session_id_fkey'),
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('interview_summaries_pkey')),
    )
    op.create_index(
        op.f('ix_interview_summaries_interview_session_id'),
        'interview_summaries',
        ['interview_session_id'],
        unique=True,
    )

    op.create_table(
        'answers',
        sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('question_id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('answer_text', sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column('submission_type', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
        sa.Column('answer_duration_seconds', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['question_id'],
            ['questions.id'],
            name=op.f('answers_question_id_fkey'),
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('answers_pkey')),
    )
    op.create_index(op.f('ix_answers_question_id'), 'answers', ['question_id'], unique=True)

    op.drop_table('interview_questions')
    op.drop_table('interviews')
