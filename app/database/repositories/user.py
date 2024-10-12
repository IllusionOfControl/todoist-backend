import uuid

from sqlalchemy import select, insert, delete

from app.core.secutiry import generate_salt, get_password_hash
from app.database.repositories.base import BaseRepository
from app.models.user import User


class UserRepository(BaseRepository):
    async def get_by_uid(self, uid: str) -> User | None:
        query = select(User).where(User.uid == uid)

        if user := await self._session.scalar(query):
            return user

    async def get_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)

        if user := await self._session.scalar(query):
            return user

    async def get_by_email(self, *, email: str) -> User | None:
        query = select(User).where(User.email == email)

        if user := await self._session.scalar(query):
            return user

    async def create(
            self,
            username: str,
            email: str,
            password: str
    ) -> User:
        password_salt = generate_salt()
        query = insert(User).values(
            uid=uuid.uuid4().hex,
            username=username,
            email=email,
            password_hash=get_password_hash(password_salt + password),
            password_salt=password_salt,
        ).returning(User)

        result = await self._session.execute(query)
        return result.scalar()

    async def delete(self, uid: int) -> User:
        query = delete(User).where(User.uid == uid).returning(User)
        result = await self._session.execute(query)
        return result.scalar()
