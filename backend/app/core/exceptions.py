"""Domain exceptions raised by services.

These are caught by global handlers registered in ``app.main`` and mapped
to proper HTTP status codes (400 / 401 / 404 / 409) instead of 500s.
"""


class AppError(Exception):
    """Base class for all application-level errors."""


class AuthenticationError(AppError):
    """Invalid credentials or missing/invalid token."""


class ResourceNotFoundError(AppError):
    """A requested resource (resume, interview, question) does not exist."""


class ResourceAlreadyExistsError(AppError):
    """A resource that must be unique already exists (e.g. duplicate email)."""


class ValidationError(AppError):
    """User input or domain state is invalid (empty PDF, wrong role, ...)."""


class ResumeNotFoundError(ResourceNotFoundError):
    """The user has not uploaded a resume yet."""


class InterviewNotFoundError(ResourceNotFoundError):
    """The interview does not exist or belongs to another user."""


class QuestionNotFoundError(ResourceNotFoundError):
    """The question does not exist or belongs to another interview."""
