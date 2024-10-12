from typing import Annotated

from fastapi import Depends

from app.api.dependencies.services import AuthenticationServiceDep
from app.core.security import TodoistTokenHeader
from app.models.user import User

__all__ = [
    "JWTTokenDep",
    "JWTTokenOptionalDep",
    "CurrentUserDep",
    "CurrentOptionalUserDep",
]

token_security = TodoistTokenHeader(
    name="Authorization",
    scheme_name="JWT Token",
    description="Token Format: `Token xxxxxx.yyyyyyy.zzzzzz`",
    raise_error=True,
)
token_security_optional = TodoistTokenHeader(
    name="Authorization",
    scheme_name="JWT Token",
    description="Token Format: `Token xxxxxx.yyyyyyy.zzzzzz`",
    raise_error=False,
)

JWTTokenDep = Annotated[str, Depends(token_security)]
JWTTokenOptionalDep = Annotated[str, Depends(token_security_optional)]


async def get_current_user_or_none(
    token: JWTTokenOptionalDep, user_service: AuthenticationServiceDep
):
    if token:
        current_user = await user_service.get_current_user(token=token)
        return current_user


async def get_current_user(
    token: JWTTokenDep, user_service: AuthenticationServiceDep
) -> User:
    current_user = await user_service.get_current_user(token=token)
    return current_user


CurrentOptionalUserDep = Annotated[User | None, Depends(get_current_user_or_none)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
