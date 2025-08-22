import typer
import mregpy

from rich.markdown import Markdown
from rich.console import Console
from rich.progress import Progress

from .scan import Scanner

cli = typer.Typer(
    no_args_is_help=True,
)
console = Console()

@cli.command("scan")
def main(directory:str):
    with Progress(console=console,transient=False,expand=True) as progress:
        Scanner(progress).scan(directory)

@cli.command("version")
def version():
    console.print(mregpy.__version__)

@cli.command("about")
def about():
    if mregpy.__doc__:
        to_render = Markdown(mregpy.__doc__)
        console.print(to_render)
        return
    raise TypeError(f"{__package__} somehow lost its documentation")

def launch():
    cli()