from datetime import datetime, date

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uid: Mapped[str] = mapped_column(unique=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    content: Mapped[str] = mapped_column(nullable=False)
    is_finished: Mapped[bool] = mapped_column(default=False)
    scheduled_at: Mapped[date] = mapped_column(nullable=True, default=None)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=False)
