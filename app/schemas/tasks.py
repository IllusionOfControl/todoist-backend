from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class TaskData(BaseModel):
    uid: str = Field(description="unique task id")
    content: str = Field(description="task content")
    is_finished: bool = Field(description="is finished flag")
    scheduled_at: date | None = Field(description="schedule date")
    created_at: datetime = Field(description="task creation date")
    updated_at: datetime = Field(description="task update date")


class TaskToUpdate(BaseModel):
    content: str | None = Field(None, description="task content")
    is_finished: bool | None = Field(None, description="is finished flag")
    scheduled_at: date | None = Field(None, description="schedule date")


class TaskToCreate(BaseModel):
    content: str = Field(..., description="task content")
    is_finished: bool = Field(..., description="is finished flag")
    scheduled_at: date | None = Field(None, description="schedule date")


class TaskInResponse(BaseModel):
    id: str
    project_id: int
    title: str = Field(title="Task title")
    is_finished: bool = Field(default=False, title="Is finished")
    scheduled_at: Optional[date] = ""


class TaskInUpdate(BaseModel):
    title: Optional[str]
    scheduled_at: Optional[date]


class ProjectInUpdate(BaseModel):
    title: Optional[str]
    scheduled_at: Optional[date]


class ListOfTasksInResponse(BaseModel):
    tasks: List[TaskInResponse]
    count: int
