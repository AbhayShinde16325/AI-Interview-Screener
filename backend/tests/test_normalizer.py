import unittest

from app.ai.interview.normalizer import QuestionNormalizer


class TestQuestionNormalizer(unittest.TestCase):

    def test_missing_fields_get_defaults(self):
        data = {"questions": [{"question": "What is a decorator?"}]}
        normalized = QuestionNormalizer.normalize(data)
        question = normalized["questions"][0]

        self.assertEqual(question["id"], 1)
        self.assertEqual(question["type"], "Conceptual")
        self.assertEqual(question["difficulty"], "Medium")
        self.assertEqual(question["expected_topics"], [])
        self.assertEqual(question["knowledge_source"], "generated")

    def test_type_mapping_normalizes_variants(self):
        data = {
            "questions": [
                {"type": "Scenario-based"},
                {"type": "Project Discussion"},
                {"type": "Coding"},
                {"type": "Unknown"},
            ]
        }
        normalized = QuestionNormalizer.normalize(data)
        types = [q["type"] for q in normalized["questions"]]
        self.assertEqual(types, ["Scenario", "Scenario", "Coding", "Conceptual"])

    def test_ids_are_assigned_in_order(self):
        data = {"questions": [{"question": "a"}, {"question": "b"}]}
        normalized = QuestionNormalizer.normalize(data)
        ids = [q["id"] for q in normalized["questions"]]
        self.assertEqual(ids, [1, 2])

    def test_existing_id_is_kept(self):
        data = {"questions": [{"id": 7, "question": "a"}]}
        normalized = QuestionNormalizer.normalize(data)
        self.assertEqual(normalized["questions"][0]["id"], 7)

    def test_mcq_variants_normalize_to_mcq(self):
        data = {
            "questions": [
                {"type": "Multiple Choice", "question": "a"},
                {"type": "Multiple-choice", "question": "b"},
                {"type": "MCQ", "question": "c"},
            ]
        }
        normalized = QuestionNormalizer.normalize(data)
        types = [q["type"] for q in normalized["questions"]]
        self.assertEqual(types, ["MCQ", "MCQ", "MCQ"])

    def test_mcq_defaults_options_and_correct_answer(self):
        data = {
            "questions": [{"type": "MCQ", "question": "a"}]
        }
        normalized = QuestionNormalizer.normalize(data)
        question = normalized["questions"][0]
        self.assertEqual(question["options"], [])
        self.assertEqual(question["correct_answer"], "")

    def test_mcq_options_are_kept(self):
        data = {
            "questions": [
                {
                    "type": "MCQ",
                    "question": "a",
                    "options": ["x", "y", "z", "w"],
                    "correct_answer": "y",
                }
            ]
        }
        normalized = QuestionNormalizer.normalize(data)
        question = normalized["questions"][0]
        self.assertEqual(
            question["options"],
            ["x", "y", "z", "w"],
        )
        self.assertEqual(question["correct_answer"], "y")


if __name__ == "__main__":
    unittest.main()
