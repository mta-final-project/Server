from typing import Annotated

import boto3
from fastapi import Depends

from src.core.settings import get_settings
from src.services.users import CognitoService


def cognito_client() -> boto3.client:
    return boto3.client("cognito-idp", region_name="us-east-1")


def cognito_client_id() -> str:
    return get_settings().cognito.client_id


def cognito_service(
    client: Annotated[boto3.client, Depends(cognito_client)],
    client_id: Annotated[str, Depends(cognito_client_id)],
) -> CognitoService:
    return CognitoService(client, client_id)
