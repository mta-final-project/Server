from typing import Self

from pydantic import BaseModel, EmailStr, Field


UserAttribute = dict[str, str]


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class CreateUserSchema(LoginSchema):
    first_name: str
    last_name: str


class ConfirmEmailSchema(BaseModel):
    email: EmailStr
    confirmation_code: str


class LoginSuccessResponse(BaseModel):
    access_token: str = Field(..., validation_alias="AccessToken")
    expires_in: int = Field(..., validation_alias="ExpiresIn")
    token_type: str = Field(..., validation_alias="TokenType")
    refresh_token: str = Field(..., validation_alias="RefreshToken")
    id_token: str = Field(..., validation_alias="IdToken")


class UserSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

    @classmethod
    def from_cognito(cls, attributes: list[UserAttribute]) -> Self:
        return cls(
            email=next(
                (attr["Value"] for attr in attributes if attr["Name"] == "email"), None
            ),
            first_name=next(
                (attr["Value"] for attr in attributes if attr["Name"] == "given_name"),
                None,
            ),
            last_name=next(
                (attr["Value"] for attr in attributes if attr["Name"] == "family_name"),
                None,
            ),
        )
