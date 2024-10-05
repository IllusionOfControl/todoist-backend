from fastapi import APIRouter, Body
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.api.dependencies.services import AuthenticationServiceDep
from app.schemas import SignInRequest, SignInResult
from app.schemas.response import TodoistResponse

router = APIRouter(
    prefix="/api",
    tags=["Authentication"]
)


@router.post(
    '/signin',
    status_code=HTTP_200_OK,
    response_model=TodoistResponse[SignInResult],
    name="User Sign In"
)
async def sign_in(
        authentication_service: AuthenticationServiceDep,
        request: SignInRequest = Body(...),
) -> TodoistResponse[SignInResult]:
    return authentication_service.handle_sign_in(request)


@router.post(
    '/signup',
    status_code=HTTP_201_CREATED,
    response_model=TodoistResponse[SignInResult],
    name="User Sign Up"
)
async def sign_in(
        authentication_service: AuthenticationServiceDep,
        request: SignInRequest = Body(...),
) -> TodoistResponse[SignInResult]:
    return authentication_service.handle_sign_up(request)
