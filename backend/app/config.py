from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://d2r_tracker:d2r_tracker_pass@db:5432/d2r_run_tracker"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
