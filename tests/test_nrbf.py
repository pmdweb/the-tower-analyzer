from __future__ import annotations

from io import BytesIO

import pytest

from tower_analyzer.parser.nrbf import NrbfParseError, read_stream_header


def _int32(value: int) -> bytes:
    return value.to_bytes(4, "little", signed=True)


def test_reads_stream_header() -> None:
    payload = b"\x00" + _int32(1) + _int32(-1) + _int32(1) + _int32(0)

    header = read_stream_header(BytesIO(payload))

    assert header.root_id == 1
    assert header.header_id == -1
    assert header.major_version == 1
    assert header.minor_version == 0


def test_rejects_invalid_first_record() -> None:
    with pytest.raises(NrbfParseError, match="SerializedStreamHeader"):
        read_stream_header(BytesIO(b"\x06" + b"\x00" * 16))


def test_rejects_truncated_header() -> None:
    with pytest.raises(NrbfParseError, match="Truncated"):
        read_stream_header(BytesIO(b"\x00\x01"))
