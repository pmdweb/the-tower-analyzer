"""CLI entry point for The Tower Save Analyzer.

Commands
--------
tower-analyzer analyze <playerInfo.dat>
    Print a summary of the save file to the terminal.

tower-analyzer export-json <playerInfo.dat> [--output account.json]
    Export the full parsed save to JSON.

tower-analyzer report <playerInfo.dat> [--output report.md]
    Generate a Markdown report.

tower-analyzer compare <old.dat> <new.dat> [--output diff.md]
    Compare two save snapshots.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table

from tower_analyzer import __version__
from tower_analyzer.analysis.comparator import SaveComparator
from tower_analyzer.analysis.summary import SaveSummary
from tower_analyzer.parser.pipeline import ParserPipeline
from tower_analyzer.reports.base import ReportContext
from tower_analyzer.reports.json_exporter import JsonExporter
from tower_analyzer.reports.markdown_report import MarkdownReport

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = typer.Typer(
    name="tower-analyzer",
    help="The Tower Save Analyzer - read-only analysis tool for The Tower save files.",
    add_completion=False,
    rich_markup_mode="rich",
)

console = Console()
err_console = Console(stderr=True)


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(console=err_console, show_path=False)],
    )


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"tower-analyzer {__version__}")
        raise typer.Exit


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            "-V",
            callback=_version_callback,
            is_eager=True,
            help="Show version and exit.",
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable debug logging."),
    ] = False,
) -> None:
    """The Tower Save Analyzer - read-only analysis tool."""
    _setup_logging(verbose)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


@app.command()
def analyze(
    save_file: Annotated[
        Path,
        typer.Argument(help="Path to playerInfo.dat", exists=True, readable=True),
    ],
) -> None:
    """Analyze a save file and print a summary to the terminal."""
    pipeline = ParserPipeline()

    with console.status(f"Parsing [bold]{save_file}[/bold]…"):
        try:
            save = pipeline.parse(save_file)
        except Exception as exc:
            err_console.print(f"[red]Error:[/red] {exc}")
            raise typer.Exit(1) from exc

    summary = SaveSummary.from_save_data(save)

    table = Table(title=f"Save Analysis - {save_file.name}", show_header=True)
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")

    table.add_row("Player Name", summary.player_name)
    table.add_row("Level", str(summary.level))
    table.add_row("Prestige", str(summary.prestige))
    table.add_row("Highest Wave", str(summary.highest_wave))
    table.add_row("File Size", f"{save.raw_bytes_size:,} bytes")
    table.add_row("Parse Warnings", str(len(summary.parse_warnings)))

    console.print(table)

    if summary.parse_warnings:
        console.print(
            Panel("\n".join(summary.parse_warnings), title="⚠ Parse Warnings", style="yellow")
        )


@app.command(name="export-json")
def export_json(
    save_file: Annotated[
        Path,
        typer.Argument(help="Path to playerInfo.dat", exists=True, readable=True),
    ],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Output JSON file path (default: account.json)"),
    ] = None,
) -> None:
    """Export the parsed save to a structured JSON file (account.json)."""
    output_path = output or Path("account.json")

    pipeline = ParserPipeline()
    exporter = JsonExporter()

    with console.status(f"Parsing [bold]{save_file}[/bold]…"):
        try:
            save = pipeline.parse(save_file)
        except Exception as exc:
            err_console.print(f"[red]Error:[/red] {exc}")
            raise typer.Exit(1) from exc

    exporter.export(save, output_path)
    console.print(f"[green]✓[/green] Exported to [bold]{output_path}[/bold]")

    if save.parse_warnings:
        console.print(
            f"[yellow]⚠[/yellow] {len(save.parse_warnings)} parse warning(s) - "
            "some fields may be at placeholder defaults."
        )


@app.command()
def report(
    save_file: Annotated[
        Path,
        typer.Argument(help="Path to playerInfo.dat", exists=True, readable=True),
    ],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Output Markdown file path (default: report.md)"),
    ] = None,
) -> None:
    """Generate a Markdown analysis report."""
    output_path = output or Path("report.md")

    pipeline = ParserPipeline()
    reporter = MarkdownReport()

    with console.status(f"Parsing [bold]{save_file}[/bold]…"):
        try:
            save = pipeline.parse(save_file)
        except Exception as exc:
            err_console.print(f"[red]Error:[/red] {exc}")
            raise typer.Exit(1) from exc

    ctx = ReportContext(save=save, output_path=output_path)
    reporter.write(ctx, output_path)
    console.print(f"[green]✓[/green] Report written to [bold]{output_path}[/bold]")


@app.command()
def compare(
    old_file: Annotated[
        Path,
        typer.Argument(help="Path to the older playerInfo.dat", exists=True, readable=True),
    ],
    new_file: Annotated[
        Path,
        typer.Argument(help="Path to the newer playerInfo.dat", exists=True, readable=True),
    ],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Output Markdown diff file path (default: diff.md)"),
    ] = None,
) -> None:
    """Compare two save file snapshots and show differences."""
    output_path = output or Path("diff.md")

    pipeline = ParserPipeline()
    comparator = SaveComparator()

    with console.status("Parsing save files…"):
        try:
            old_save = pipeline.parse(old_file)
            new_save = pipeline.parse(new_file)
        except Exception as exc:
            err_console.print(f"[red]Error:[/red] {exc}")
            raise typer.Exit(1) from exc

    diff = comparator.compare(old_save, new_save)

    console.print(Panel(
        "\n".join(diff.notes) if diff.notes else "No differences detected.",
        title=f"Diff: {old_file.name} → {new_file.name}",
        style="blue",
    ))

    # Write a minimal diff report
    diff_md = [
        f"# Save Diff: `{old_file.name}` → `{new_file.name}`\n",
        "",
        "## Notes\n",
        "",
    ]
    for note in diff.notes:
        diff_md.append(f"- {note}")

    output_path.write_text("\n".join(diff_md), encoding="utf-8")
    console.print(f"[green]✓[/green] Diff written to [bold]{output_path}[/bold]")


def run() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    run()
