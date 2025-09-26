import click
from . import tasks


@click.group()
def cli() -> None:
    """Dobrydo CLI entrypoint."""
    pass

@click.group()
def task() -> None:
    """Task commands."""
    pass

task.add_command(tasks.create)
task.add_command(tasks.list)

cli.add_command(task)
