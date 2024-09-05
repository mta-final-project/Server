import boto3
from fastapi import Request

from src.api.users.schemas import (
    CreateUserSchema,
    LoginSchema,
    LoginSuccessResponse,
    UserSchema,
)
from src.models import User


class CognitoService:
    def __init__(self, client: boto3.client, client_id: str):
        self._client = client
        self._client_id = client_id

    async def register(self, params: CreateUserSchema) -> None:
        response = self._client.sign_up(
            ClientId=self._client_id,
            Username=params.email,
            Password=params.password,
            UserAttributes=[
                {"Name": "given_name", "Value": params.first_name},
                {"Name": "family_name", "Value": params.last_name},
            ],
        )
        new_user = User(cognito_id=response["UserSub"], email=params.email)
        await new_user.save()

    def resend_confirmation_email(self, email: str) -> None:
        self._client.resend_confirmation_code(ClientId=self._client_id, Username=email)

    async def delete_user(self, token: str) -> None:
        user_info = self.get_user_info(token)
        self._client.delete_user(
            AccessToken=token,
        )
        user = await User.find_one(email=user_info.email)
        await user.delete()

    def login(self, params: LoginSchema) -> LoginSuccessResponse:
        response = self._client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": params.email, "PASSWORD": params.password},
            ClientId=self._client_id,
        )
        return LoginSuccessResponse(**response["AuthenticationResult"])

    def get_user_info(self, token: str) -> UserSchema:
        response = self._client.get_user(
            AccessToken=token,
        )

        return UserSchema.from_cognito(response["UserAttributes"])

    async def get_user_by_token(self, token: str) -> User:
        user_info = self.get_user_info(token)
        return await User.find_one(email=user_info.email)

    async def get_user_by_request(self, request: Request) -> User:
        token = self.get_auth_token(request)
        return await self.get_user_by_token(token)

    @staticmethod
    def get_auth_token(request: Request) -> str:
        return request.headers.get("Authorization").split(" ")[1]
