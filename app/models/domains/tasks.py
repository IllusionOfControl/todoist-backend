from pydantic import BaseModel
from datetime import datetime, date


class TaskDomain(BaseModel):
    id: str
    project_id: int
    title: str
    is_finished: bool
    scheduled_at: date = ""
    created_at: datetime
    updated_at: datetime
