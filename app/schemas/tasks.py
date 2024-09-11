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


class TaskInResponse(BaseModel):
    id: str
    project_id: int
    title: str = Field(title="Task title")
    is_finished: bool = Field(default=False, title="Is finished")
    scheduled_at: Optional[date] = ""


class TaskInCreate(BaseModel):
    title: str


class TaskInUpdate(BaseModel):
    title: Optional[str]
    scheduled_at: Optional[date]


class ProjectInUpdate(BaseModel):
    title: Optional[str]
    scheduled_at: Optional[date]


class ListOfTasksInResponse(BaseModel):
    tasks: List[TaskInResponse]
    count: int
