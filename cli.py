import click
from src.job_templates import get_job_templates


@click.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")


@click.command()
def templates():
    """List Job Templates"""
    available_job_templates = get_job_templates()
    for idx, template in enumerate(available_job_templates):
        print(f"{idx+1}. {template}")


if __name__ == '__main__':
    templates()
