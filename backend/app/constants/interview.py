from enum import Enum


class Role(str, Enum):
    AI_ML_ENGINEER = "AI_ML_ENGINEER"
    BACKEND_ENGINEER = "BACKEND_ENGINEER"
    DATA_ENGINEER = "DATA_ENGINEER"
    PYTHON_DEVELOPER = "PYTHON_DEVELOPER"
    FULL_STACK_DEVELOPER = "FULL_STACK_DEVELOPER"


class InterviewStatus(str, Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"


class QuestionDifficulty(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class QuestionSource(str, Enum):
    RESUME = "RESUME"
    KNOWLEDGE_BASE = "KNOWLEDGE_BASE"
    MIXED = "MIXED"

class SubmissionType(str, Enum):
    TEXT = "TEXT"
    MCQ = "MCQ"

class Recommendation(str, Enum):
    HIRE = "HIRE"
    BORDERLINE = "BORDERLINE"
    NO_HIRE = "NO_HIRE"