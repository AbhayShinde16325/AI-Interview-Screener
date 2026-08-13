from uuid import UUID

from pydantic import BaseModel, field_validator

SUPPORTED_ROLES = {
    "AI/ML Engineer",
    "Backend Engineer",
    "Data Engineer",
    "Python Developer",
    "Full Stack Developer",
}


class StartInterviewRequest(BaseModel):
    role: str

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        value = value.strip()
        if value not in SUPPORTED_ROLES:
            raise ValueError(
                f"Unsupported role '{value}'. Supported roles: "
                f"{', '.join(sorted(SUPPORTED_ROLES))}."
            )
        return value


class SubmitAnswerRequest(BaseModel):
    question_id: UUID
    answer: str
