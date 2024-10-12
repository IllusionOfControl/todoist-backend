from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class TaskData(BaseModel):
    uid: str = Field(description="unique task id")
    content: str = Field(description="task content")
    is_finished: bool = Field(description="is finished flag")
    scheduled_at: date | None = Field(description="schedule date")
    created_at: datetime = Field(description="task creation date")
    updated_at: datetime = Field(description="task update date")


class TaskEditRequest(BaseModel):
    content: str = Field(..., description="task content")
    is_finished: bool = Field(..., description="is finished flag")
    scheduled_at: date | None = Field(None, description="schedule date")
