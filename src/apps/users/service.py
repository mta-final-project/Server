import boto3

from src.apps.users.api.schemas import (
    CreateUserSchema,
    LoginSchema,
    LoginSuccessResponse,
    UserSchema,
)


class CognitoService:
    def __init__(self, client: boto3.client, client_id: str):
        self._client = client
        self._client_id = client_id

    def register(self, params: CreateUserSchema) -> None:
        _ = self._client.sign_up(
            ClientId=self._client_id,
            Username=params.email,
            Password=params.password,
            UserAttributes=[
                {"Name": "given_name", "Value": params.first_name},
                {"Name": "family_name", "Value": params.last_name},
            ],
        )

    def login(self, params: LoginSchema) -> LoginSuccessResponse:
        response = self._client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": params.email, "PASSWORD": params.password},
            ClientId=self._client_id,
        )
        return LoginSuccessResponse(**response["AuthenticationResult"])

    def get_user(self, token: str) -> UserSchema:
        response = self._client.get_user(
            AccessToken=token,
        )

        return UserSchema.from_cognito(response["UserAttributes"])
