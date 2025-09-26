import click

@click.command()
@click.argument("title")
@click.option("--content", help="Task description")
@click.option("--due", help="Task due date")
def create(title: str, content: str, due: str) -> None:
    """Create a new task with TITLE, CONTENT, and DUE date."""
    click.echo(f"Created task with title '{title}', content '{content}', and date '{due}'")

create: click.Command

@click.command()
@click.option("--due", help="Task due date")
def list(due: str):
    """List all tasks."""
    click.echo("All tasks.")

list: click.Command
