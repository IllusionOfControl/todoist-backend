from app.core.exceptions import NotFoundError, AuthError, BadRequestError
from app.core.secutiry import verify_password
from app.database.repositories.users import UsersRepository
from app.resourses import strings
from app.schemas import SignInResponse, SignInRequest, SignUpRequest
from app.services.jwt import JWTService


class AuthenticationService:
    def __init__(self, user_repository: UsersRepository, jwt_service: JWTService):
        self._user_repository = user_repository
        self._jwt_service = jwt_service

    async def check_username_is_taken(self, username: str) -> bool:
        user = await self._user_repository.get_by_username(username=username)
        return user is not None

    async def check_email_is_taken(self, email: str) -> bool:
        user = await self._user_repository.get_by_email(email=email)
        return user is not None

    async def handle_sign_in(self, *, request: SignInRequest) -> SignInResponse:
        user = await self._user_repository.get_by_username(request.username)
        if user is None:
            raise NotFoundError(f"user with username {request.username} not found")

        if not verify_password(user.password_salt + request.password, user.password_hash):
            raise AuthError("login or password is incorrect")

        token = self._jwt_service.create_access_token_for_user(
            user,
        )

        # TODO: Make refresh token
        return SignInResponse(
            username=user.username,
            user_id=str(user.id),
            access_token=token,
            refresh_token="",
            # refresh_token=token,
        )

    async def handle_sign_up(self, *, request: SignUpRequest) -> SignInResponse:
        if await self.check_username_is_taken(request.username):
            raise BadRequestError(strings.USERNAME_TAKEN)

        if await self.check_email_is_taken(request.email):
            raise BadRequestError(strings.EMAIL_TAKEN)

        user = await self._user_repository.create(
            username=request.username,
            email=request.email,
            password=request.password,
        )

        # TODO: Make refresh token
        token = self._jwt_service.create_access_token_for_user(
            user,
        )
        return SignInResponse(
            username=user.username,
            user_id=str(user.id),
            access_token=token,
            refresh_token="",
            # refresh_token=token,
        )
