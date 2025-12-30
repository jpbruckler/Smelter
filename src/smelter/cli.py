from __future__ import annotations
from pathlib import Path
from typing import Annotated
import sys
import pprint
import typer
from smelter.extract_text import extract_text
from smelter.extract_text import parse_pages

app = typer.Typer(
    help="Smelter CLI - A PDF text extraction tool",
    add_completion=False,
)

@app.callback(invoke_without_command=True)
def root(ctx: typer.Context):
    """
    Smelter CLI - A PDF text extraction tool
    """
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()

@app.command()
def convert(
    pdf: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
    pages: Annotated[
        str | None,
        typer.Option(
            "--pages",
            help="Pages to extract (e.g. '1-5', '2,4,6'). 1-based.",
        ),
    ] = None,
    output: Annotated[
        Path | None,
        typer.Option("-o", "--output", help="Write to a file instead of stdout."),
    ] = None,
    debug: Annotated[bool, typer.Option("--debug", help="Enable debug mode.")] = False,
):
    """
    Extract text from a PDF file.
    """
    page_list: list[int] | None = None
    if pages:
        # open PDF once to know page count
        import fitz
        with fitz.open(pdf) as doc:
            page_list = parse_pages(pages, doc.page_count)
    
    extracted = extract_text(pdf, pages=page_list)
    if not isinstance(extracted, dict):
        raise TypeError("extract_text() must return dict[int, str]")
    
    if output:
        combined = "".join(extracted[p] for p in sorted(extracted))
        output.write_text(combined, encoding="utf-8")
    else:
        if debug:
            pprint.pprint(extracted, indent=4, sort_dicts=False)
        else:
            for page_number in sorted(extracted):
                sys.stdout.write(extracted[page_number])


def entrypoint() -> None:
    app()
