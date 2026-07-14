"""Tests for the parser pipeline."""

from __future__ import annotations

from pathlib import Path

import pytest

from tower_analyzer.models.save_data import SaveData
from tower_analyzer.parser.pipeline import ParserPipeline


class TestParserPipeline:
    """Integration-level tests for the full parser pipeline."""

    def test_parse_minimal_save(self, gzip_save_file: Path) -> None:
        """Pipeline should complete without error on a minimal valid save."""
        pipeline = ParserPipeline()
        result = pipeline.parse(gzip_save_file)
        assert isinstance(result, SaveData)

    def test_parse_records_source_file(self, gzip_save_file: Path) -> None:
        """SaveData should contain the source file path."""
        pipeline = ParserPipeline()
        result = pipeline.parse(gzip_save_file)
        assert result.source_file == str(gzip_save_file)

    def test_parse_records_file_size(self, gzip_save_file: Path) -> None:
        """SaveData should record the original compressed file size."""
        pipeline = ParserPipeline()
        result = pipeline.parse(gzip_save_file)
        assert result.raw_bytes_size == gzip_save_file.stat().st_size

    def test_parse_missing_file_raises(self, tmp_path: Path) -> None:
        """Pipeline should raise FileNotFoundError for missing files."""
        pipeline = ParserPipeline()
        with pytest.raises(FileNotFoundError):
            pipeline.parse(tmp_path / "missing.dat")

    def test_parse_has_warnings(self, gzip_save_file: Path) -> None:
        """Pipeline should emit at least one parse warning while decode is incomplete."""
        pipeline = ParserPipeline()
        result = pipeline.parse(gzip_save_file)
        assert len(result.parse_warnings) > 0
