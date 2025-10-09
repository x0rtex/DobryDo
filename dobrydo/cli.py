"""DobryDo CLI Productivity Suite."""

import click

from .commands import task_command
from .db import init_db


@click.group()
def cli() -> None:
    """DobryDo CLI Productivity Suite."""
    init_db()


@click.group()
def task() -> None:
    """Task commands."""
    pass


task.add_command(task_command.add)
task.add_command(task_command.list_tasks)
task.add_command(task_command.complete)
task.add_command(task_command.delete)
cli.add_command(task)


@click.group()
def note() -> None:
    """Note commands."""
    pass


cli.add_command(note)


@click.group()
def timer() -> None:
    """Timer commands."""
    pass


cli.add_command(timer)
