from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.tasks import TaskData


class ProjectInfo(BaseModel):
    uid: int
    title: str
    description: str
    color: str


class ProjectCreateRequest(BaseModel):
    title: str
    description: str
    color: int

## Response


class ProjectData(BaseModel):
    uid: str = Field(..., description="Unique identifier for the project")
    title: str = Field(..., description="Title of the project")
    description: str = Field(..., description="Description of the project")
    color: int = Field(..., description="Color code associated with the project")
    tasks: list[TaskData] = Field(default_factory=list, description="List of tasks")


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


class ProjectInResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = ""


class ProjectInUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]


class ListOfProjectsInResponse(BaseModel):
    projects: List[ProjectInResponse]
    count: int
