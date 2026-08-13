import unittest

from app.ai.interview.generator import QuestionGenerator


class TestQuestionGeneratorParseJson(unittest.TestCase):

    def test_wrapped_object_is_kept(self):
        raw = '{"questions": [{"id": 1}]}'
        data = QuestionGenerator._parse_json(raw)
        self.assertEqual(data, {"questions": [{"id": 1}]})

    def test_bare_array_is_wrapped(self):
        raw = '[{"id": 1}, {"id": 2}]'
        data = QuestionGenerator._parse_json(raw)
        self.assertEqual(data, {"questions": [{"id": 1}, {"id": 2}]})

    def test_fenced_bare_array_is_wrapped(self):
        raw = '```json\n[{"id": 1}]\n```'
        data = QuestionGenerator._parse_json(raw)
        self.assertEqual(data, {"questions": [{"id": 1}]})

    def test_bare_array_survives_normalization_and_validation(self):
        from app.ai.interview.normalizer import QuestionNormalizer
        from app.schemas.interview import InterviewQuestionList

        raw = '[{"skill": "Python", "type": "Conceptual", "difficulty": "Easy", "question": "What is a list?", "expected_topics": ["lists"]}]'
        data = QuestionNormalizer.normalize(QuestionGenerator._parse_json(raw))
        result = InterviewQuestionList.model_validate(data)
        self.assertEqual(len(result.questions), 1)
        self.assertEqual(result.questions[0].id, 1)


if __name__ == "__main__":
    unittest.main()
