from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ResumeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    filename: str
    created_at: datetime


class LatestResumeResponse(BaseModel):
    """Latest resume for a user, including the parsed summary + skills."""

    id: UUID
    filename: str
    created_at: datetime
    summary: str
    skills: list[str]
