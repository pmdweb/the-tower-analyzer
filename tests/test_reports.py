"""Tests for report generation and JSON export."""

from __future__ import annotations

import json
from pathlib import Path

from tower_analyzer.models.player_account import PlayerAccount
from tower_analyzer.models.save_data import SaveData
from tower_analyzer.reports.base import ReportContext
from tower_analyzer.reports.json_exporter import JsonExporter
from tower_analyzer.reports.markdown_report import MarkdownReport


class TestMarkdownReport:
    """Tests for MarkdownReport."""

    def test_generate_returns_string(self, empty_save_data: SaveData) -> None:
        report = MarkdownReport()
        ctx = ReportContext(save=empty_save_data)
        result = report.generate(ctx)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_report_contains_heading(self, empty_save_data: SaveData) -> None:
        report = MarkdownReport()
        ctx = ReportContext(save=empty_save_data)
        result = report.generate(ctx)
        assert "# The Tower Save Analyzer" in result

    def test_report_includes_player_section(self, empty_save_data: SaveData) -> None:
        report = MarkdownReport()
        ctx = ReportContext(save=empty_save_data)
        result = report.generate(ctx)
        assert "## Player Account" in result

    def test_report_includes_warnings(self) -> None:
        save = SaveData(source_file="test.dat", parse_warnings=["Test warning"])
        report = MarkdownReport()
        ctx = ReportContext(save=save)
        result = report.generate(ctx)
        assert "Test warning" in result

    def test_write_creates_file(self, tmp_path: Path, empty_save_data: SaveData) -> None:
        out = tmp_path / "report.md"
        report = MarkdownReport()
        ctx = ReportContext(save=empty_save_data, output_path=out)
        report.write(ctx, out)
        assert out.exists()
        assert out.stat().st_size > 0

    def test_name_property(self) -> None:
        report = MarkdownReport()
        assert isinstance(report.name, str)
        assert len(report.name) > 0


class TestJsonExporter:
    """Tests for JsonExporter."""

    def test_export_creates_file(self, tmp_path: Path, empty_save_data: SaveData) -> None:
        exporter = JsonExporter()
        out = tmp_path / "account.json"
        exporter.export(empty_save_data, out)
        assert out.exists()

    def test_export_valid_json(self, tmp_path: Path, empty_save_data: SaveData) -> None:
        exporter = JsonExporter()
        out = tmp_path / "account.json"
        exporter.export(empty_save_data, out)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert "source_file" in data
        assert "account" in data

    def test_export_source_file_preserved(self, tmp_path: Path) -> None:
        save = SaveData(source_file="my_save.dat")
        exporter = JsonExporter()
        out = tmp_path / "account.json"
        exporter.export(save, out)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["source_file"] == "my_save.dat"

    def test_to_json_str(self, empty_save_data: SaveData) -> None:
        exporter = JsonExporter()
        result = exporter.to_json_str(empty_save_data)
        assert isinstance(result, str)
        data = json.loads(result)
        assert "account" in data

    def test_export_nested_player(self, tmp_path: Path) -> None:
        save = SaveData(
            source_file="x.dat",
            account=PlayerAccount(player_name="Charlie", level=99),
        )
        exporter = JsonExporter()
        out = tmp_path / "account.json"
        exporter.export(save, out)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["account"]["player_name"] == "Charlie"
        assert data["account"]["level"] == 99
