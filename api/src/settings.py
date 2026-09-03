from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    # api
    APP_NAME: str = ""
    CORS_ORIGINS: str = ""

    # listmonk
    LISTMONK_URL: str = ""
    LISTMONK_USER: str = ""
    LISTMONK_PASS: str = ""
    LISTMONK_LIST: int = 0
    LISTMONK_TEMPLATE_WELCOME_EMAIL: int = 0

    # gotify
    GOTIFY_URL: str = ""
    GOTIFY_PASS: str = ""

    # database
    POSTGRES_DB: str = ""
    POSTGRES_HOST: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""

    @property
    def CORS_ORIGIN_LIST(self) -> list[str]:
        return [
            origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()
        ]

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:5432/{self.POSTGRES_DB}"


settings = Settings()
