import pytest

from app.core.exceptions import UsernameAlreadyTakenException, EmailAlreadyTakenException, IncorrectLoginInputException, UserNotFoundException
from app.schemas import SignInRequest, SignUpRequest
from app.services.authentication import AuthenticationService


@pytest.mark.asyncio
async def test_check_username_is_taken(authentication_service: AuthenticationService, test_user):
    assert await authentication_service.check_username_is_taken("testuser") is True
    assert await authentication_service.check_username_is_taken("nonexistentuser") is False


@pytest.mark.asyncio
async def test_check_email_is_taken(authentication_service: AuthenticationService, test_user):
    assert await authentication_service.check_email_is_taken("testuser@example.com") is True
    assert await authentication_service.check_email_is_taken("nonexistentemail@example.com") is False


@pytest.mark.asyncio
async def test_handle_sign_in_successful(authentication_service: AuthenticationService, test_user):
    sign_in_request = SignInRequest(username="testuser", password="testpassword")
    sign_in_response = await authentication_service.handle_sign_in(request=sign_in_request)
    assert sign_in_response.username == "testuser"
    assert sign_in_response.access_token is not None


@pytest.mark.asyncio
async def test_handle_sign_in_wrong_password(authentication_service: AuthenticationService, test_user):
    sign_in_request = SignInRequest(username="testuser", password="wrongpassword")
    with pytest.raises(IncorrectLoginInputException):
        await authentication_service.handle_sign_in(request=sign_in_request)


@pytest.mark.asyncio
async def test_handle_sign_in_user_not_found(authentication_service: AuthenticationService):
    sign_in_request = SignInRequest(username="nonexistentuser", password="somepassword")
    with pytest.raises(UserNotFoundException):
        await authentication_service.handle_sign_in(request=sign_in_request)


@pytest.mark.asyncio
async def test_handle_sign_up_successful(authentication_service: AuthenticationService):
    sign_up_request = SignUpRequest(
        username="newuser",
        email="newuser@example.com",
        password="newpassword"
    )
    sign_in_response = await authentication_service.handle_sign_up(request=sign_up_request)
    assert sign_in_response.username == "newuser"
    assert sign_in_response.access_token is not None


@pytest.mark.asyncio
async def test_handle_sign_up_username_taken(authentication_service: AuthenticationService, test_user):
    sign_up_request = SignUpRequest(
        username="testuser",
        email="newuser@example.com",
        password="newpassword"
    )
    with pytest.raises(UsernameAlreadyTakenException):
        await authentication_service.handle_sign_up(request=sign_up_request)


@pytest.mark.asyncio
async def test_handle_sign_up_email_taken(authentication_service: AuthenticationService, test_user):
    sign_up_request = SignUpRequest(
        username="newuser",
        email="testuser@example.com",
        password="newpassword"
    )
    with pytest.raises(EmailAlreadyTakenException):
        await authentication_service.handle_sign_up(request=sign_up_request)