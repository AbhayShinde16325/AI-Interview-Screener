class QuestionNormalizer:

    TYPE_MAPPING = {
        "Scenario-based": "Scenario",
        "Scenario Based": "Scenario",
        "Scenario": "Scenario",
        "Coding": "Coding",
        "Conceptual": "Conceptual",
    }

    DIFFICULTY_MAPPING = {
        "Easy": "Easy",
        "Medium": "Medium",
        "Hard": "Hard",
    }

    @classmethod
    def normalize(cls, data: dict) -> dict:

        for question in data["questions"]:

            question["type"] = cls.TYPE_MAPPING.get(
                question["type"],
                question["type"],
            )

            question["difficulty"] = cls.DIFFICULTY_MAPPING.get(
                question["difficulty"],
                question["difficulty"],
            )

        return data