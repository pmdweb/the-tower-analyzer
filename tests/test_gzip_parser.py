"""Tests for GzipParser."""

from __future__ import annotations

import gzip
import io
from pathlib import Path

import pytest

from tower_analyzer.parser.gzip_parser import GzipParseError, GzipParser


class TestGzipParser:
    """Unit tests for GzipParser."""

    def test_decompress_valid_file(self, gzip_save_file: Path) -> None:
        """GzipParser should decompress a valid GZip file."""
        parser = GzipParser()
        data = parser.decompress(gzip_save_file)
        assert isinstance(data, bytes)
        assert len(data) > 0

    def test_decompress_roundtrip(self, tmp_path: Path) -> None:
        """Compressed data should round-trip through GzipParser."""
        payload = b"hello tower"
        gz_path = tmp_path / "test.dat"

        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
            gz.write(payload)
        gz_path.write_bytes(buf.getvalue())

        parser = GzipParser()
        result = parser.decompress(gz_path)
        assert result == payload

    def test_decompress_bytes_roundtrip(self) -> None:
        """decompress_bytes should recover original payload."""
        payload = b"binary formatter data"
        compressed = gzip.compress(payload)
        parser = GzipParser()
        assert parser.decompress_bytes(compressed) == payload

    def test_decompress_missing_file(self, tmp_path: Path) -> None:
        """decompress should raise FileNotFoundError for missing files."""
        parser = GzipParser()
        with pytest.raises(FileNotFoundError):
            parser.decompress(tmp_path / "nonexistent.dat")

    def test_decompress_invalid_gzip(self, tmp_path: Path) -> None:
        """decompress should raise GzipParseError for non-GZip files."""
        bad_file = tmp_path / "bad.dat"
        bad_file.write_bytes(b"this is not gzip data")
        parser = GzipParser()
        with pytest.raises(GzipParseError):
            parser.decompress(bad_file)

    def test_decompress_bytes_invalid(self) -> None:
        """decompress_bytes should raise GzipParseError for bad bytes."""
        parser = GzipParser()
        with pytest.raises(GzipParseError):
            parser.decompress_bytes(b"not gzip")
