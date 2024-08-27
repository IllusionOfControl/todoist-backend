from app.core.exceptions import NotFoundError, AuthError, BadRequestError
from app.db.errors import EntityDoesNotExist
from app.db.repositories.users import UsersRepository
from app.models.schemas.authentication import SignInResponse, SignInRequest, SignUpRequest
from app.resourses import strings
from app.services.jwt import JWTService


class AuthenticationService:
    def __init__(self, user_repository: UsersRepository, jwt_service: JWTService):
        self._user_repository = user_repository
        self._jwt_service = jwt_service

    async def check_username_is_taken(self, username: str) -> bool:
        try:
            await self._user_repository.get_user_by_username(username=username)
        except EntityDoesNotExist:
            return False
        return True

    async def check_email_is_taken(self, email: str) -> bool:
        try:
            await self._user_repository.get_user_by_email(email=email)
        except EntityDoesNotExist:
            return False
        return True

    async def handle_sign_in(self, *, request: SignInRequest) -> SignInResponse:
        try:
            user = await self._user_repository.get_user_by_username(request.username)
        except EntityDoesNotExist as err:
            raise NotFoundError(f"user with username {request.username} not found")

        if not user.check_password(request.password):
            raise AuthError("login or password is incorrect")

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

    async def handle_sign_up(self, *, request: SignUpRequest) -> SignInResponse:
        if await self.check_username_is_taken(request.username):
            raise BadRequestError(strings.USERNAME_TAKEN)

        if await self.check_email_is_taken(request.email):
            raise BadRequestError(strings.EMAIL_TAKEN)

        user = await self._user_repository.create_user(
            username=request.username,
            email=request.email,
            password=request.password,
        )

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
