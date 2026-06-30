from pydantic import BaseModel


class Education(BaseModel):
    degree: str
    institution: str
    graduation_year: str | None = None


class Experience(BaseModel):
    company: str
    role: str
    duration: str


class Project(BaseModel):
    title: str
    description: str
    technologies: list[str]


class ParsedResume(BaseModel):
    summary: str
    skills: list[str]
    education: list[Education]
    experience: list[Experience]
    projects: list[Project]
    certifications: list[str]
    keywords: list[str]