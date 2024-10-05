from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.api.dependencies.services import AuthenticationServiceDep
from app.schemas import SignInRequest, SignInData, SignUpRequest
from app.schemas.response import TodoistResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    '/signin',
    status_code=HTTP_200_OK,
    response_model=TodoistResponse[SignInData],
)
async def sign_in(
        authentication_service: AuthenticationServiceDep,
        request: SignInRequest,
) -> TodoistResponse[SignInData]:
    access_token = await authentication_service.sign_in_user(request)
    return TodoistResponse[SignInData](
        success=True,
        data=SignInData(
            access_token=access_token,
        )
    )


@router.post(
    '/signup',
    status_code=HTTP_201_CREATED,
    response_model=TodoistResponse[SignInData],
)
async def sign_up(
        authentication_service: AuthenticationServiceDep,
        request: SignUpRequest,
) -> TodoistResponse[SignInData]:
    access_token = await authentication_service.sign_up_user(request.username, request.email, request.password)
    return TodoistResponse[SignInData](
        success=True,
        data=SignInData(
            access_token=access_token,
        )
    )
