from fastapi import APIRouter, Depends, Request, status

from src.api.common.deps import UsersServiceDep
from src.api.users.schemas import (
    CreateUserSchema,
    LoginSchema,
    LoginSuccessResponse,
)
from src.core.auth import cognito_auth

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
async def register(params: CreateUserSchema, service: UsersServiceDep) -> None:
    await service.register(params)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(params: LoginSchema, service: UsersServiceDep) -> LoginSuccessResponse:
    return service.login(params)


@router.get(
    "/current-user",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(cognito_auth)],
)
async def get_current_user(request: Request, service: UsersServiceDep):
    # Auth token must be present because of the cognito_auth dependency
    token = service.get_auth_token(request)

    return service.get_user_info(token)


@router.delete(
    "/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(cognito_auth)],
)
async def delete_user(request: Request, service: UsersServiceDep) -> None:
    token = service.get_auth_token(request)
    await service.delete_user(token)
