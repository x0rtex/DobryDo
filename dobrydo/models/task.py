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


@dataclass
class Note:
    id: int
    title: str
    content: str | None
    created_at: datetime.datetime
    tags: list[str] | None


@dataclass
class Timer:
    id: int
    title: str
    duration: datetime.timedelta
    created_at: datetime.datetime
    completed_at: datetime.datetime | None
