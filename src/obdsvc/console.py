import click
from . import __version__
@click.command()
@click.version_option(version=__version__)
def main():
    """A service to relay OBD2 info onto a seperate application message bus."""
    click.echo("Hello, world!")