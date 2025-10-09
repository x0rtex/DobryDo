"""Task commands for DobryDo CLI."""

import click
from datetime import datetime, date

from dobrydo.db.db import get_session
from dobrydo.models.task import Task


def validate_due_date(
    _ctx: click.Context, _param: click.Parameter, date_str: str | None
) -> date | None:
    """Validate and parse due date from DD/MM/YYYY format."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError:
        raise click.BadParameter(f"Due date must be in DD/MM/YYYY format. Got: {date_str}")


@click.command()
@click.argument("title")
@click.option("--content", "--c", help="Task content")
@click.option("--duedate", "--d", help="Task due date (DD/MM/YYYY)", callback=validate_due_date)
@click.option("--tags", "--t", help="Tags related to task", multiple=True)
def add(title: str, content: str | None, duedate: date | None, tags: tuple[str]) -> None:
    """Add a new task."""
    with get_session() as session:
        task: Task = Task(
            title=title,
            content=content,
            due_date=duedate,
            tags=list(tags) if tags else None,
        )
        session.add(task)
        session.flush()

        click.echo(f"Added task: {task.title} (ID: {task.id})")


@click.command()
def list_tasks() -> None:
    """List all tasks."""
    with get_session() as session:
        tasks: list[Task] = session.query(Task).order_by(Task.created_at.desc()).all()

        if not tasks:
            click.echo("No tasks found.")
            return

        for task in tasks:
            click.echo(f"[{task.id}] {task.title}")


@click.command()
@click.argument("id", type=int)
def delete(id: int) -> None:
    """Delete a task by ID."""
    with get_session() as session:
        task: Task | None = session.get(Task, id)

        if not task:
            click.echo(f"Error: No task found with ID {id}")
            return

        session.delete(task)

    click.echo(f"Deleted task: [{id}] {task.title}")
