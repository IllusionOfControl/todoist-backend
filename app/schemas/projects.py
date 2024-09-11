from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.tasks import TaskData


class ProjectData(BaseModel):
    uid: int
    title: str
    description: str
    color: str
    tasks: list[TaskData] = Field(default_factory=list, description="List of tasks")


class ProjectInfo(BaseModel):
    uid: int
    title: str
    description: str
    color: str


#######


class ProjectCreateResult(BaseModel):
    id: int
    uuid: str
    title: str
    color: str

class ProjectRetrieveResult(BaseModel):
    id: int
    uuid: str
    title: str
    color: str
    tasks


class ProjectInResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = ""


class ProjectInCreate(BaseModel):
    title: str


class ProjectInUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]


class ListOfProjectsInResponse(BaseModel):
    projects: List[ProjectInResponse]
    count: int
