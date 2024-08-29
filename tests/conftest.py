import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_app_settings
from app.core.application import Application
from app.database.database import database
from app.database.repositories.users import UsersRepository
from app.models.users import User
from app.services.authentication import AuthenticationService
from app.services.jwt import JWTService


@pytest.fixture(scope="session")
def application() -> Application:
    return Application()


@pytest_asyncio.fixture(scope="session")
async def initialized_app(application: Application):
    async with LifespanManager(application.fastapi_app) as manager:
        yield manager.app


@pytest_asyncio.fixture
async def session(initialized_app: FastAPI) -> AsyncSession:
    settings = get_app_settings()
    database.connect(settings.database)

    async with database.session() as session:
        yield session


@pytest_asyncio.fixture
async def test_user(session: AsyncSession) -> User:
    repo = UsersRepository(session)
    user = await repo.create(
        "testuser",
        "testuser@example.com",
        "testpassword",
    )
    yield user

    await repo.delete(user.id)


@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
            app=initialized_app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest_asyncio.fixture
async def authentication_service(session: AsyncSession) -> AuthenticationService:
    repo = UsersRepository(session)
    jwt_service = JWTService("testsecret")
    return AuthenticationService(repo, jwt_service)
