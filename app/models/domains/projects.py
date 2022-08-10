from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProjectDomain(BaseModel):
    id: str
    owner_id: int
    title: str
    description: Optional[str] = ""
    created_at: datetime
    updated_at: datetime
