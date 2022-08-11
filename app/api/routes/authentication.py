from fastapi import APIRouter, Depends, Body, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.resourses import strings
from app.models.schemas.users import UserInSignin, UserInResponse, UserInSignup
from app.db.repositories.users import UsersRepository
from app.services.authentication import check_email_is_taken, check_username_is_taken
from app.services.jwt import create_access_token_for_user

router = APIRouter()


@router.post(
    '/signin',
    response_model=UserInResponse,
    name="auth:sign-in"
)
async def login_user(
    user_login: UserInSignin = Body(...),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: AppSettings = Depends(get_app_settings)
) -> UserInResponse:
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail=strings.INCORRECT_LOGIN_INPUT,
    )

    try:
        user = await user_repo.get_user_by_username(username=user_login.username)
    except EntityDoesNotExist as existence_error:
        raise wrong_login_error from existence_error

    if not user.check_password(user_login.password):
        raise wrong_login_error

    token = create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value())
    )
    return UserInResponse(**user.dict(), token=token)


@router.post(
    '/signup',
    status_code=HTTP_201_CREATED,
    response_model=UserInResponse,
    name="auth:sign-up"
)
async def register_user(
    user_signup: UserInSignup = Body(...),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: AppSettings = Depends(get_app_settings)
) -> UserInResponse:
    if await check_username_is_taken(users_repo, user_signup.username):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.USERNAME_TAKEN,
        )

    if await check_email_is_taken(users_repo, user_signup.email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.EMAIL_TAKEN,
        )
    user = await users_repo.create_user(**user_signup.dict())

    token = create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value())
    )
    return UserInResponse(**user.dict(), token=token)
