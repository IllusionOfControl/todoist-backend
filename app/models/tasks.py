from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class TaskDomain(BaseModel):
    id: int
    project_id: int
    title: str
    is_finished: bool
    scheduled_at: Optional[date] = ""
    created_at: datetime
    updated_at: datetime
