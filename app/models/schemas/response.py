from typing import Generic, TypeVar

from pydantic import BaseModel, Field

__all__ = ["TodoistResponse"]

T = TypeVar('T')


class TodoistResponse(BaseModel, Generic[T]):
    success: bool = Field(description='successful/unsuccessful flag')
    message: str = Field(description='error message')
    data: T = Field(description="object data")
