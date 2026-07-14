from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from tower_analyzer.parser import inspect_save
from tower_analyzer.parser.save_inspector import SaveInspectionError

app = typer.Typer(help="Read-only analyzer for The Tower Android save files.")
console = Console()


@app.command()
def inspect(path: Path) -> None:
    """Inspect compression and payload metadata without deserializing the save."""
    try:
        result = inspect_save(path)
    except SaveInspectionError as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(code=1) from exc

    table = Table(title="The Tower save inspection")
    table.add_column("Property")
    table.add_column("Value")
    table.add_row("Path", str(result.path))
    table.add_row("Compression", result.compression)
    table.add_row("Compressed size", f"{result.compressed_size:,} bytes")
    table.add_row("Decompressed size", f"{result.decompressed_size:,} bytes")
    table.add_row("Payload", result.payload_type)
    table.add_row("SHA-256", result.sha256)
    console.print(table)


@app.command("export-json")
def export_json(path: Path) -> None:
    """Export parsed account data when the NRBF parser is implemented."""
    del path
    console.print("[yellow]Not implemented: NRBF object-graph parsing is required first.[/yellow]")


@app.command()
def report(path: Path) -> None:
    """Generate a report when account mapping is implemented."""
    del path
    console.print("[yellow]Not implemented: account mapping is required first.[/yellow]")


@app.command()
def compare(old: Path, new: Path) -> None:
    """Compare two saves when structured export is implemented."""
    del old, new
    console.print("[yellow]Not implemented: structured snapshots are required first.[/yellow]")


if __name__ == "__main__":
    app()
