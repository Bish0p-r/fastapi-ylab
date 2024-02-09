from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    MODE: Literal['DEV', 'TEST', 'PROD'] = 'DEV'

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def db_uri(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def test_db_uri(self):
        return (
            f'postgresql+asyncpg://{self.TEST_DB_USER}:'
            f'{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:'
            f'{self.TEST_DB_PORT}/{self.TEST_DB_NAME}'
        )

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_TEST_HOST: str
    CACHE_TTL: int = 180

    GOOGLE_SHEETS_ID: str

    @property
    def google_sheets_url(self):
        return f'https://docs.google.com/spreadsheets/d/{self.GOOGLE_SHEETS_ID}/export?format=xlsx'

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str = 'guest'
    RABBITMQ_PASS: str = 'guest'

    @property
    def rabbitmq_amqp_url(self):
        return f'amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}'

    @property
    def rabbitmq_rpc_url(self):
        return f'rpc://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}'


settings = Settings()
