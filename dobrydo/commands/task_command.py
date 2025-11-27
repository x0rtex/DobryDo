"""Task commands for DobryDo CLI."""

from datetime import date, datetime

import click

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
@click.argument("id", type=int)
@click.option("--title", "--ti", help="Task title")
@click.option("--content", "--c", help="Task content")
@click.option("--duedate", "--d", help="Task due date (DD/MM/YYYY)", callback=validate_due_date)
@click.option("--tags", "--t", help="Tags related to task", multiple=True)
def edit(
    id: int, title: str | None, content: str | None, duedate: date | None, tags: tuple[str]
) -> None:
    """Edit existing task by ID."""
    with get_session() as session:
        task: Task | None = session.get(Task, id)

        if not task:
            click.echo(f"Task with ID {id} not found.")
            return

        if title:
            task.title = title
        if content:
            task.content = content
        if duedate:
            task.due_date = duedate
        if tags:
            task.tags = list(tags)

        click.echo(f"Edited task: {task.title} (ID: {task.id})")


@click.command(name="list")
def list_tasks() -> None:
    """List all tasks."""
    with get_session() as session:
        tasks: list[Task] = session.query(Task).order_by(Task.created_at.desc()).all()

        if not tasks:
            click.echo("No tasks found.")
            return

        for task in tasks:
            status: str = "Completed" if task.is_completed else "Incomplete"
            if task.is_overdue:
                status += " (Overdue)"
            click.echo(f"[{task.id}] {status}: {task.title}")


@click.command()
@click.argument("id", type=int)
def complete(id: int) -> None:
    """Mark a task as completed."""
    with get_session() as session:
        task: Task | None = session.get(Task, id)

        if not task:
            click.echo(f"Error: No task found with ID {id}")
            return

        if task.is_completed:
            click.echo(f"Error: Task {id} is already completed.")
            return

        task.completed_at = datetime.now()
        task_title: str = task.title

    click.echo(f"Completed task: [{id}] {task_title}")


@click.command()
@click.argument("id", type=int)
def info(id: int) -> None:
    """Show task information by ID."""
    with get_session() as session:
        task: Task | None = session.get(Task, id)

        if not task:
            click.echo(f"Error: No task found with ID {id}")
            return

        click.echo(f"Task ID: {task.id}")
        click.echo(f"Title: {task.title}")

        if task.content:
            click.echo(f"\nContent:\n{task.content}")

        click.echo(f"\nCreated: {task.created_at.strftime('%d/%m/%Y %H:%M:%S')}")

        if task.due_date:
            due_date_str: str = task.due_date.strftime("%d/%m/%Y")
            if task.is_overdue and not task.is_completed:
                click.echo(f"Due Date: {due_date_str} (OVERDUE)", err=True)
            else:
                click.echo(f"Due Date: {due_date_str}")

        if task.completed_at:
            click.echo(f"Completed: {task.completed_at.strftime('%d/%m/%Y %H:%M:%S')}")
        else:
            click.echo("Status: Incomplete")

        if task.tags:
            click.echo(f"Tags: {', '.join(task.tags)}")


@click.command()
@click.argument("id", type=int)
def delete(id: int) -> None:
    """Delete a task by ID."""
    with get_session() as session:
        task: Task | None = session.get(Task, id)

        if not task:
            click.echo(f"Error: No task found with ID {id}")
            return

        task_title: str = task.title
        session.delete(task)

    click.echo(f"Deleted task: [{id}] {task_title}")
