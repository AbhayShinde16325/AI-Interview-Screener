from app.ai.prompts.interview_questions import (
    QUESTION_GENERATION_PROMPT,
)
from app.ai.resume_parser.schemas import ParsedResume


class PromptBuilder:
    """
    Builds the interview question generation prompt.
    """

    def build(
        self,
        resume: ParsedResume,
        skill: str,
        knowledge_context: str,
        question_count: int,
    ) -> str:

        project_names = [
            project.title
            for project in resume.projects
        ]

        resume_summary = f"""
Summary:
{resume.summary}

Projects:
{", ".join(project_names)}

Candidate Skills:
{", ".join(resume.skills)}
"""

        return QUESTION_GENERATION_PROMPT.format(
            skill=skill,
            knowledge=knowledge_context,
            count=question_count,
            resume_summary=resume_summary,
        )