"""Task model for DobryDo."""

from datetime import datetime, date

from sqlalchemy import String, Date, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column

from dobrydo.db import Base


class Task(Base):
    """Task model representing a todo item."""

    __tablename__: str = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str | None] = mapped_column(String, nullable=True)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(), nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    tags: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    @property
    def is_completed(self) -> bool:
        return self.completed_at is not None

    @property
    def is_overdue(self) -> bool:
        return self.due_date is not None and self.due_date < date.today()
