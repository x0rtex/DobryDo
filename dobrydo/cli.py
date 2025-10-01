import click
from .tools import tasks, notes, timers


@click.group()
def cli() -> None:
    """Dobrydo CLI entrypoint."""
    pass

@click.group()
def task() -> None:
    """Task commands."""
    pass

task.add_command(tasks.add)
task.add_command(tasks.list)
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

