from app.core.exceptions import UserNotFoundException, IncorrectLoginInputException, UsernameAlreadyTakenException, EmailAlreadyTakenException
from app.core.secutiry import verify_password
from app.database.repositories.users import UsersRepository
from app.resourses import strings
from app.schemas import SignInResult, SignInRequest, SignUpRequest
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

    async def handle_sign_in(self, *, request: SignInRequest) -> SignInResult:
        user = await self._user_repository.get_by_username(request.username)
        if user is None:
            raise UserNotFoundException()

        if not verify_password(user.password_salt + request.password, user.password_hash):
            raise IncorrectLoginInputException()

        token = self._jwt_service.create_access_token_for_user(
            user,
        )

        # TODO: Make refresh token
        return SignInResult(
            username=user.username,
            user_id=str(user.id),
            access_token=token,
            refresh_token="",
            # refresh_token=token,
        )

    async def handle_sign_up(self, *, request: SignUpRequest) -> SignInResult:
        if await self.check_username_is_taken(request.username):
            raise UsernameAlreadyTakenException(strings.USERNAME_TAKEN)

        if await self.check_email_is_taken(request.email):
            raise EmailAlreadyTakenException(strings.EMAIL_TAKEN)

        user = await self._user_repository.create(
            username=request.username,
            email=request.email,
            password=request.password,
        )

        # TODO: Make refresh token
        token = self._jwt_service.create_access_token_for_user(
            user,
        )
        return SignInResult(
            username=user.username,
            user_id=str(user.id),
            access_token=token,
            refresh_token="",
            # refresh_token=token,
        )
