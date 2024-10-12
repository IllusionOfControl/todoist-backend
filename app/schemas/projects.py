from pydantic import BaseModel, Field


class ProjectInfo(BaseModel):
    uid: int = Field(..., description="Unique identifier for the project")
    title: str = Field(..., description="Title of the project")
    description: str = Field(..., description="Description of the project")
    color: str = Field(..., description="Color code associated with the project")


class ProjectEditRequest(BaseModel):
    title: str = Field(..., description="Title of the project")
    description: str = Field(..., description="Description of the project")
    color: str = Field(..., description="Color code associated with the project")


class ProjectData(BaseModel):
    uid: str = Field(..., description="Unique identifier for the project")
    title: str = Field(..., description="Title of the project")
    description: str = Field(..., description="Description of the project")
    color: int = Field(..., description="Color code associated with the project")
