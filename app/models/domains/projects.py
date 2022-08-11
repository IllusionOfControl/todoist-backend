from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProjectDomain(BaseModel):
    id: int
    owner_id: int
    title: str
    description: Optional[str] = ""
    created_at: datetime
    updated_at: datetime
