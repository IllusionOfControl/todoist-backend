from app.db.repositories.base import BaseRepository
from app.db.errors import EntityDoesNotExist
from app.models.domains.users import UserDomain


class UsersRepository(BaseRepository):
    async def get_user_by_username(self, *, username: str) -> UserDomain:
        sql = """ SELECT * FROM users WHERE users.username=($1) """

        user_row = await self.connection.fetch(sql, username)
        if user_row:
            return UserDomain(**dict(*user_row))

        raise EntityDoesNotExist("user with username {0} does not exist".format(username))

    async def get_user_by_email(self, *, email: str) -> UserDomain:
        sql = """ SELECT * FROM users WHERE users.email=$1 """
        query = await self.connection.prepare(sql)

        user_row = await query.fetchval(email)
        if user_row:
            return UserDomain(**dict(*user_row))

        raise EntityDoesNotExist("user with email {0} does not exist".format(email))

    async def create_user(
        self,
        *,
        username: str,
        email: str,
        password: str
    ) -> UserDomain:
        sql = """ INSERT INTO users (username, email, password_hash, password_salt)
VALUES (($1), ($2), ($3), ($4)) RETURNING *; """

        user = UserDomain(username=username, email=email)
        user.change_password(password)

        user_row = await self.connection.fetch(
            sql,
            user.username,
            user.email,
            user.password_hash,
            user.password_salt
        )

        return user.copy(update=dict(*user_row))
