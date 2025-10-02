import datetime
from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    content: str | None
    due_date: datetime.date | None
    created_at: datetime.datetime
    completed_at: datetime.datetime | None
    tags: list[str] | None
