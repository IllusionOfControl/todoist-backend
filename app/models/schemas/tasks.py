from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class TaskInResponse(BaseModel):
    id: str
    project_id: int
    title: str
    is_finished: bool
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
    projects: List[TaskInResponse]
    count: int
