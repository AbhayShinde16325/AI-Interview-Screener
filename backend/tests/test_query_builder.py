import unittest

from app.ai.resume_parser.schemas import ParsedResume
from app.ai.retrieval.retriever import QueryBuilder


def make_resume(skills, keywords):
    return ParsedResume(
        summary="summary",
        skills=skills,
        education=[],
        experience=[],
        projects=[],
        certifications=[],
        keywords=keywords,
    )


class TestQueryBuilder(unittest.TestCase):

    def test_query_contains_skill(self):
        resume = make_resume(["Python"], ["Python", "FastAPI"])
        query = QueryBuilder.for_skill("Python", resume)
        self.assertIn("Python", query)

    def test_query_uses_candidate_keywords(self):
        resume = make_resume(
            ["Python"],
            ["Python", "Django", "FastAPI"],
        )
        query = QueryBuilder.for_skill("Python", resume)
        self.assertIn("Django", query)
        self.assertIn("FastAPI", query)

    def test_query_keeps_mentioning_keywords(self):
        resume = make_resume(
            ["Machine Learning"],
            ["Machine Learning", "TensorFlow"],
        )
        query = QueryBuilder.for_skill("Machine Learning", resume)
        self.assertIn("TensorFlow", query)

    def test_query_with_no_keywords_is_just_skill(self):
        resume = make_resume(["Python"], [])
        query = QueryBuilder.for_skill("Python", resume)
        self.assertEqual(query, "Python")


if __name__ == "__main__":
    unittest.main()
