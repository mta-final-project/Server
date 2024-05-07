from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class MongoSettings(BaseModel):
    url: str = "mongodb://user:pass@localhost:27017"
    database: str = "courses"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    api: ApiSettings = ApiSettings()
    mongo: MongoSettings = MongoSettings()


@lru_cache
def get_settings():
    return Settings()
