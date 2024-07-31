from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi_cognito import CognitoAuth as _CognitoAuth, CognitoSettings, CognitoToken

from src.core.settings import get_settings


class CognitoAuth(HTTPBearer):
    def __init__(self, settings: CognitoSettings):
        super().__init__()
        self.auth = _CognitoAuth(
          settings=settings, userpool_name="default"
        )

    async def __call__(self, request: Request) -> CognitoToken:
        return await self.auth.auth_required(request=request)


cognito_auth = CognitoAuth(
    settings=CognitoSettings.from_global_settings(get_settings().cognito)
)
