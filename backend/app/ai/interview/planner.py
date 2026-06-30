from app.ai.resume_parser.schemas import ParsedResume


class InterviewPlanner:
    """
    Creates a deterministic interview plan from a parsed resume.
    """

    MAX_TECHNICAL_SKILLS = 4
    QUESTIONS_PER_SKILL = 2
    PROJECT_QUESTIONS = 2

    def create_plan(
        self,
        resume: ParsedResume,
    ) -> dict:

        skills = resume.skills[
            : self.MAX_TECHNICAL_SKILLS
        ]

        plan = []

        for skill in skills:

            plan.append(
                {
                    "skill": skill,
                    "questions": self.QUESTIONS_PER_SKILL,
                }
            )

        if resume.projects:

            plan.append(
                {
                    "skill": "Projects",
                    "questions": self.PROJECT_QUESTIONS,
                }
            )

        return {
            "total_questions": sum(
                item["questions"]
                for item in plan
            ),
            "plan": plan,
        }