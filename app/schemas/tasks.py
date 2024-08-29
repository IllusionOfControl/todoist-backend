from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List


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
