from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str
    database_url: str
    gemini_api_key: str
    # JWT
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # AI
    gemini_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()