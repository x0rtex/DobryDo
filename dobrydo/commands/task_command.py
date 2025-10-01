from datetime import datetime
import json
import click
import sqlite3


def create_table_if_not_exists(cur: sqlite3.Cursor) -> None:
    _ = cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            details TEXT,
            due_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            tags TEXT
        );
    """
    )


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
@click.option("--details", "--d", help="Task details")
@click.option("--duedate", "--due", help="Task due date", callback=validate_due_date)
@click.option("--tags", "--t", help="Tags related to task", multiple=True)
def add(title: str, details: str, duedate: str, tags: tuple[str]) -> None:
    """Add a new task with TITLE, DETAILS, TAGS, and DUE date."""
    tags_json: str = json.dumps(tags)
    with sqlite3.connect("dobrydo.db") as conn:
        cur = conn.cursor()
        create_table_if_not_exists(cur)

        _ = cur.execute(
            """
            INSERT INTO tasks (title, details, due_date, tags)
            VALUES (?, ?, ?, ?)
        """,
            (title, details, duedate, tags_json),
        )

    click.echo(
        f"Added task with title '{title}', details '{details}', and due date of '{duedate}' with tags '{tags}'."
    )


@click.command()
def list() -> None:
    """List all tasks."""
    click.echo(f"All tasks.")
    click.echo(
        "Task ID | Title | Details | Due Date | Created At | Completed At | Tags"
    )
    click.echo("---------------------------------------------------------------")
    with sqlite3.connect("dobrydo.db") as conn:
        cur = conn.cursor()
        create_table_if_not_exists(cur)

        _ = cur.execute(
            """
            SELECT id, title, details, due_date, created_at, completed_at, tags
            FROM tasks
        """,
        )

        tasks = cur.fetchall()
        for task in tasks:
            click.echo(
                f"{task[0]} | {task[1]} | {task[2]} | {task[3]} | {task[4]} | {task[5]} | {task[6]}"
            )


@click.command()
@click.argument("id", type=int)
def delete(id: int) -> None:
    """Delete a specified task by ID."""
    with sqlite3.connect("dobrydo.db") as conn:
        cur = conn.cursor()
        create_table_if_not_exists(cur)

        _ = cur.execute(
            """
            DELETE FROM tasks WHERE id = ?
        """,
            (id,),
        )
        conn.commit()

    click.echo(f"Task with ID {id} has been deleted.")
