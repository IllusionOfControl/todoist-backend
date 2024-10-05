from typing import Iterable

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas.response import TodoistResponse


class BaseInternalException(Exception):
    _status_code: int = 0
    _message: str = ''
    _errors: Iterable[str] | None = None

    def __init__(self, status_code: int | None = None, message: str | None = None, errors: Iterable[str] = None):
        self._status_code = status_code
        self._message = message
        self._errors = errors

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def message(self) -> str:
        return self._message

    @property
    def errors(self) -> Iterable[str] | None:
        return self._errors


class IncorrectLoginInputException(BaseInternalException):
    _status_code = 400
    _message = "incorrect username or password."


class UserNotFoundException(BaseInternalException):
    _status_code = 404
    _message = "user with this username does not exist."


class ProjectNotFoundException(BaseInternalException):
    _status_code = 404
    _message = "project with this id does not exist."


class ProjectPermissionException(BaseInternalException):
    _status_code = 403
    _message = "you do not have permission to access this project."


class TaskNotFoundException(BaseInternalException):
    _status_code = 404
    _message = "task with this id does not exist."


class TaskPermissionException(BaseInternalException):
    _status_code = 403
    _message = "you do not have permission to access this task."


class EmailAlreadyTakenException(BaseInternalException):
    _status_code = 400
    _message = "email is already taken."


class UsernameAlreadyTakenException(BaseInternalException):
    _status_code = 400
    _message = "username is already taken."


def add_internal_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(BaseInternalException)
    async def _exception_handler(
            _: Request, exc: BaseInternalException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=TodoistResponse(
                success=False,
                message=exc.message,
                errors=exc.errors
            )
        )


def add_request_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def _exception_handler(
            _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=TodoistResponse(
                success=False,
                message="schema validation error",
                errors=exc.errors(),
            )
        )


def add_exception_handlers(app: FastAPI) -> None:
    add_internal_exception_handler(app)
    add_request_exception_handler(app)
