from typing import Annotated

from fastapi import APIRouter, status, Depends

from src.core.auth import JWTAuthCredentials, JWTBearer
from src.apps.users.schemas import (
    LoginSchema,
    CreateUserSchema,
    LoginSuccessResponse,
)
from src.apps.users.service import CognitoService
from src.apps.users.deps import cognito_service

router = APIRouter(prefix="/users", tags=["users"])

auth = JWTBearer()


ServiceDep = Annotated[
    CognitoService,
    Depends(cognito_service),
]


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
async def register(params: CreateUserSchema, service: ServiceDep) -> None:
    service.register(params)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(params: LoginSchema, service: ServiceDep) -> LoginSuccessResponse:
    return service.login(params)


@router.get("/current-user", status_code=status.HTTP_200_OK)
async def get_current_user(
    service: ServiceDep, credentials: JWTAuthCredentials = Depends(auth)
):
    return service.get_user(credentials.jwt_token)
