"""Tests for the Typer CLI."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from tower_analyzer.cli import app

runner = CliRunner()


class TestCLI:
    def test_version_flag(self) -> None:
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "tower-analyzer" in result.output

    def test_help(self) -> None:
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "analyze" in result.output

    def test_analyze_command(self, gzip_save_file: Path) -> None:
        result = runner.invoke(app, ["analyze", str(gzip_save_file)])
        assert result.exit_code == 0

    def test_export_json_command(self, gzip_save_file: Path, tmp_path: Path) -> None:
        out = tmp_path / "account.json"
        result = runner.invoke(app, ["export-json", str(gzip_save_file), "--output", str(out)])
        assert result.exit_code == 0
        assert out.exists()

    def test_report_command(self, gzip_save_file: Path, tmp_path: Path) -> None:
        out = tmp_path / "report.md"
        result = runner.invoke(app, ["report", str(gzip_save_file), "--output", str(out)])
        assert result.exit_code == 0
        assert out.exists()

    def test_compare_command(self, gzip_save_file: Path, tmp_path: Path) -> None:
        out = tmp_path / "diff.md"
        result = runner.invoke(
            app,
            ["compare", str(gzip_save_file), str(gzip_save_file), "--output", str(out)],
        )
        assert result.exit_code == 0
        assert out.exists()

    def test_analyze_missing_file(self, tmp_path: Path) -> None:
        missing = tmp_path / "missing.dat"
        result = runner.invoke(app, ["analyze", str(missing)])
        assert result.exit_code != 0

    def test_export_json_missing_file(self, tmp_path: Path) -> None:
        missing = tmp_path / "missing.dat"
        result = runner.invoke(app, ["export-json", str(missing)])
        assert result.exit_code != 0
