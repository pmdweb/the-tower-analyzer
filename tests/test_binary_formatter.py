"""Tests for BinaryFormatterParser."""

from __future__ import annotations

import struct

import pytest

from tower_analyzer.parser.binary_formatter import (
    BinaryFormatterError,
    BinaryFormatterParser,
    RawObject,
)


class TestBinaryFormatterParser:
    """Unit tests for BinaryFormatterParser."""

    def test_parse_valid_header(self, minimal_bf_bytes: bytes) -> None:
        """Parser should read a valid MS-NRBF header without raising."""
        parser = BinaryFormatterParser()
        result = parser.parse(minimal_bf_bytes)
        assert isinstance(result, RawObject)

    def test_parse_returns_raw_object(self, minimal_bf_bytes: bytes) -> None:
        """Parser should return a RawObject with expected class name."""
        parser = BinaryFormatterParser()
        result = parser.parse(minimal_bf_bytes)
        assert result.class_name == "SaveLoad.PlayerData"

    def test_parse_header_contains_metadata(self, minimal_bf_bytes: bytes) -> None:
        """Parser should attach header metadata to raw_fields."""
        parser = BinaryFormatterParser()
        result = parser.parse(minimal_bf_bytes)
        assert "_header" in result.fields
        header = result.fields["_header"]
        assert header["major_version"] == 1
        assert header["minor_version"] == 0

    def test_parse_empty_stream_raises(self) -> None:
        """Parser should raise BinaryFormatterError for empty input."""
        parser = BinaryFormatterParser()
        with pytest.raises(BinaryFormatterError, match="Empty stream"):
            parser.parse(b"")

    def test_parse_wrong_record_type_raises(self) -> None:
        """Parser should raise if stream does not start with record type 0."""
        bad = struct.pack("B", 5) + b"\x00" * 16
        parser = BinaryFormatterParser()
        with pytest.raises(BinaryFormatterError, match="Expected SerializationHeaderRecord"):
            parser.parse(bad)

    def test_parse_truncated_header_raises(self) -> None:
        """Parser should raise if header is too short."""
        truncated = struct.pack("B", 0) + b"\x00" * 4  # needs 16 bytes of body
        parser = BinaryFormatterParser()
        with pytest.raises(BinaryFormatterError, match="too short"):
            parser.parse(truncated)

    def test_parse_wrong_version_raises(self) -> None:
        """Parser should raise if BinaryFormatter version != 1.0."""
        bad = struct.pack("B", 0) + struct.pack("<iiii", 1, -1, 2, 0)
        parser = BinaryFormatterParser()
        with pytest.raises(BinaryFormatterError, match="version"):
            parser.parse(bad)

    def test_read_string_single_byte_length(self, minimal_bf_bytes: bytes) -> None:
        """_read_string should decode a 7-bit encoded length-prefixed string."""
        import io as _io

        text = "hello"
        encoded = struct.pack("B", len(text)) + text.encode("utf-8")
        reader = _io.BytesIO(encoded)
        parser = BinaryFormatterParser()
        assert parser._read_string(reader) == text
