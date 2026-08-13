class QuestionNormalizer:

    TYPE_MAPPING = {
        "Scenario-based": "Scenario",
        "Scenario Based": "Scenario",
        "Scenario": "Scenario",
        "Project Discussion": "Scenario",
        "Project-Based": "Scenario",
        "Coding": "Coding",
        "Conceptual": "Conceptual",
        "MCQ": "MCQ",
        "Multiple Choice": "MCQ",
        "Multiple-choice": "MCQ",
        "Multiple Choice Question": "MCQ",
    }

    DIFFICULTY_MAPPING = {
        "Easy": "Easy",
        "Medium": "Medium",
        "Hard": "Hard",
    }

    @classmethod
    def normalize(cls, data: dict) -> dict:

        for index, question in enumerate(data.get("questions", []), start=1):

            # Ensure every question has an id
            question["id"] = question.get("id", index)

            # Normalize question type
            question["type"] = cls.TYPE_MAPPING.get(
                question.get("type"),
                "Conceptual",
            )

            # MCQ questions must carry options + a correct answer; fill
            # empty defaults so downstream schema validation reports them
            # clearly instead of silently accepting a broken question.
            if question["type"] == "MCQ":
                if not isinstance(question.get("options"), list):
                    question["options"] = []
                if not question.get("correct_answer"):
                    question["correct_answer"] = ""

            # Normalize difficulty
            question["difficulty"] = cls.DIFFICULTY_MAPPING.get(
                question.get("difficulty"),
                "Medium",
            )

            # Ensure expected_topics exists
            if not question.get("expected_topics"):
                question["expected_topics"] = []

            # Ensure knowledge_source exists
            if not question.get("knowledge_source"):
                question["knowledge_source"] = "generated"

        return data