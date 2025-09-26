import click

@click.command()
def hello():
    click.echo('Hello World!')

def main() -> None:
    hello()


if __name__ == "__main__":
    main()
