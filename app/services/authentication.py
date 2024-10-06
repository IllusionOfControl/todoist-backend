from app.core.exceptions import UserNotFoundException, IncorrectLoginInputException, UsernameAlreadyTakenException, \
    EmailAlreadyTakenException, IncorrectJWTTokenException
from app.core.secutiry import verify_password
from app.database.repositories.users import UsersRepository
from app.models.users import User
from app.services.jwt import JWTService


class AuthenticationService:
    def __init__(self, user_repository: UsersRepository, jwt_service: JWTService):
        self._user_repository = user_repository
        self._jwt_service = jwt_service

    async def _check_username_is_taken(self, username: str) -> bool:
        user = await self._user_repository.get_by_username(username=username)
        return user is not None

    async def _check_email_is_taken(self, email: str) -> bool:
        user = await self._user_repository.get_by_email(email=email)
        return user is not None

    async def sign_in_user(self, username: str, password: str) -> str:
        user = await self._user_repository.get_by_username(username)
        if user is None:
            raise UserNotFoundException()

        if not verify_password(user.password_salt + password, user.password_hash):
            raise IncorrectLoginInputException()

        token = self._jwt_service.create_access_token_for_user(user.uid)

        # TODO: Make refresh token
        return token

    async def sign_up_user(self, username: str, email: str, password: str) -> str:
        if await self._check_username_is_taken(username):
            raise UsernameAlreadyTakenException()

        if await self._check_email_is_taken(email):
            raise EmailAlreadyTakenException()

        user = await self._user_repository.create(
            username=username,
            email=email,
            password=password,
        )

        # TODO: Make refresh token
        token = self._jwt_service.create_access_token_for_user(user.uid)
        return token

    async def get_current_user(self, token: str) -> User:
        user_uid = self._jwt_service.get_user_uid_from_token(token)
        if user := await self._user_repository.get_by_uid(user_uid):
            return user
        else:
            raise IncorrectJWTTokenException()
