import unittest

from app.ai.interview.planner import InterviewPlanner
from app.ai.resume_parser.schemas import ParsedResume


def make_resume(skills, projects=1):
    return ParsedResume(
        summary="Test summary",
        skills=skills,
        education=[],
        experience=[],
        projects=[
            {"title": f"Project {i}", "description": "desc", "technologies": ["Python"]}
            for i in range(projects)
        ],
        certifications=[],
        keywords=skills[:3],
    )


class TestInterviewPlanner(unittest.TestCase):

    def setUp(self):
        self.planner = InterviewPlanner()

    def test_plan_total_matches_questions(self):
        resume = make_resume(["Python", "ML", "SQL", "Docker", "AWS"])
        plan = self.planner.create_plan(resume)

        self.assertEqual(
            plan["total_questions"],
            sum(item["questions"] for item in plan["plan"]),
        )

    def test_max_technical_skills_capped(self):
        resume = make_resume(["s1", "s2", "s3", "s4", "s5", "s6"])
        plan = self.planner.create_plan(resume)

        skills = [item["skill"] for item in plan["plan"] if item["skill"] != "Projects"]
        self.assertEqual(len(skills), self.planner.MAX_TECHNICAL_SKILLS)

    def test_project_questions_included_when_projects_exist(self):
        resume = make_resume(["Python"])
        plan = self.planner.create_plan(resume)
        self.assertIn("Projects", [item["skill"] for item in plan["plan"]])

    def test_no_project_section_without_projects(self):
        resume = make_resume(["Python"], projects=0)
        plan = self.planner.create_plan(resume)
        self.assertNotIn("Projects", [item["skill"] for item in plan["plan"]])


if __name__ == "__main__":
    unittest.main()
