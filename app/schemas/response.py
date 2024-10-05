from typing import Generic, TypeVar, Optional, Iterable

from pydantic import BaseModel, Field

__all__ = ["TodoistResponse", "ListData"]

T = TypeVar('T')


class TodoistResponse(BaseModel, Generic[T]):
    success: bool = Field(description='successful/unsuccessful flag')
    message: Optional[str] = Field(None, description='error message')
    errors: Optional[Iterable[str]] = Field(None, description="list of errors")
    data: Optional[T] = Field(None, description="object data")


class ListData(BaseModel, Generic[T]):
    count: int = Field(..., description="Total number of items in the list")
    items: list[T] = Field(..., description="List of items")
