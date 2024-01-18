from typing import Literal

from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    MODE: Literal["DEV", "TEST", "PROD"]

    SECRET_KEY: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def db_uri(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:" f"{self.DB_PASS}@{self.DB_HOST}:" f"{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
