import json
from datetime import datetime

import click

from dobrydo.db import get_db


def validate_due_date(ctx, param, date_str: str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError:
        raise click.BadParameter(
            f"Due date must be in DD/MM/YYYY format. Got: {date_str}"
        )


@click.command()
@click.argument("title")
@click.option("--content", "--c", help="Task content")
@click.option("--duedate", "--d", help="Task due date", callback=validate_due_date)
@click.option("--tags", "--t", help="Tags related to task", multiple=True)
def add(title: str, content: str, duedate: str, tags: tuple[str]) -> None:
    """Add a new task with TITLE, DETAILS, TAGS, and DUE date."""
    tags_json: str = json.dumps(tags)
    with get_db() as conn:
        cur = conn.cursor()

        _ = cur.execute(
            """
            INSERT INTO tasks (title, content, due_date, tags)
            VALUES (?, ?, ?, ?)
        """,
            (title, content, duedate, tags_json),
        )

    click.echo(
        f"Added task with title '{title}', details '{content}', \
        and due date of '{duedate}' with tags '{tags}'."
    )


@click.command()
def list() -> None:
    """List all tasks."""
    raise NotImplementedError


@click.command()
@click.argument("id", type=int)
def delete(id: int) -> None:
    """Delete a specified task by ID."""
    with get_db() as conn:
        cur = conn.cursor()

        _ = cur.execute(
            """
            DELETE FROM tasks WHERE id = ?
        """,
            (id,),
        )
        conn.commit()

    click.echo(f"Task with ID {id} has been deleted.")
