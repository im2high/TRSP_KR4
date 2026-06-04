from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # По умолчанию используем локальный SQLite, чтобы проект
    # запускался "из коробки" без поднятия внешней БД.
    database_url: str = "sqlite:///./app.db"
    app_name: str = "FastAPI KR4"


settings = Settings()
