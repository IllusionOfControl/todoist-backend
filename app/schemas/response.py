from typing import Generic, TypeVar, Optional, Iterable

from pydantic import BaseModel, Field

__all__ = ["TodoistResponse", "ListData"]

ResponseTypeVar = TypeVar('ResponseTypeVar')
ListItemTypeVar = TypeVar('ListItemTypeVar')


class TodoistResponse(BaseModel, Generic[ResponseTypeVar]):
    success: bool = Field(description='successful/unsuccessful flag')
    message: Optional[str] = Field(None, description='error message')
    errors: Optional[Iterable[str]] = Field(None, description="list of errors")
    data: Optional[ResponseTypeVar] = Field(None, description="object data")


class ListData(BaseModel, Generic[ListItemTypeVar]):
    count: int = Field(..., description="Total number of items in the list")
    items: list[ListItemTypeVar] = Field(..., description="List of items")
