from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application configuration, loaded from environment variables."""

    # --- Database ---------------------------------------------------------
    # Prefer the full connection string (Neon / Render / local).
    # If DATABASE_URL is empty, it is assembled from the parts below.
    database_url: str = ""

    # Optional parts, used only when database_url is not set
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "interview_screener"
    database_user: str = "postgres"
    database_password: str = "postgres"

    # --- AI ----------------------------------------------------------------
    gemini_api_key: str = ""

    # --- JWT ---------------------------------------------------------------
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    # --- CORS ---------------------------------------------------------------
    # Comma-separated list of allowed frontend origins.
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # --- Application ---------------------------------------------------------
    # Directory where uploaded resumes are stored (relative to backend/).
    upload_dir: str = "uploads"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def sqlalchemy_database_url(self) -> str:
        """Connection URL used by SQLAlchemy / Alembic."""
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+psycopg2://{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
