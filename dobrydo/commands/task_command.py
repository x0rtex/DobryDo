import click
import sqlite3


@click.command()
@click.argument("title")
@click.option("--details", help="Task details")
@click.option("--due", help="Task due date")
def add(title: str, details: str, due: str) -> None:
    """Add a new task with TITLE, DETAILS, and DUE date."""
    # TODO: Implement add functionality
    with sqlite3.connect("/db/dobrydo.db") as conn:
        cur = conn.cursor()
        cur = cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title text NOT NULL,
            details text,
            due_date DATE,
            is_completed INTEGER NOT NULL DEFAULT 0
            );
        """)

        cur = cur.execute("""
            INSERT INTO tasks (title, details, due_date, is_completed) VALUES
            ('Complete SQLite tutorial', 1),
            ('Learn Boolean in SQLite', 0),
        """)

    click.echo(
        f"Added task with title '{title}', details '{details}', and date '{due}'"
    )


add: click.Command


@click.command()
@click.option("--due", help="Task due date")
def list(due: str) -> None:
    """List all tasks."""
    # TODO: Implement list functionality
    click.echo(f"All tasks. ({due})")


list: click.Command


@click.command()
@click.argument("title")
def delete(title: str) -> None:
    """Delete a specified task by name."""
    # TODO: Implement delete functionality
    click.echo(f"To delete task. ({title})")


delete: click.Command
