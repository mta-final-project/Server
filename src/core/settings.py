from functools import lru_cache
from typing import Any

from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env")


class ApiSettings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000


class MongoSettings(BaseSettings):
    url: str = "mongodb+srv://ac-user:Password1@ac-cluster.3qj8y.mongodb.net/?retryWrites=true&w=majority&appName=AC-Cluster"
    database: str = "academease"


class S3Settings(BaseSettings):
    region: str = "us-east-1"
    bucket_name: str = "academease-materials"
    presigned_url_expiration: int = 3600


class CognitoSettings(BaseSettings):
    client_id: str = "6r70ag4thnsitfb378fh87tj92"
    pool_id: str = "us-east-1_U2F78N1y3"
    region: str = "us-east-1"

    check_expiration: bool = True
    jwt_header_prefix: str = "Bearer"
    jwt_header_name: str = "Authorization"
    userpools: dict[str, dict[str, Any]] = {
        "default": {
            "region": region,
            "userpool_id": pool_id,
            "app_client_id": [client_id],
        }
    }


class Settings(BaseSettings):
    api: ApiSettings = ApiSettings()
    mongo: MongoSettings = MongoSettings()
    s3: S3Settings = S3Settings()
    cognito: CognitoSettings = CognitoSettings()


@lru_cache
def get_settings():
    return Settings()
