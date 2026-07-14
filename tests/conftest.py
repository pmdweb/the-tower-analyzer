"""Shared pytest fixtures and helpers."""

from __future__ import annotations

import gzip
import io
import struct
from pathlib import Path

import pytest

from tower_analyzer.models.save_data import SaveData

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_bf_header(root_id: int = 1, header_id: int = -1) -> bytes:
    """Build a minimal MS-NRBF serialization header record."""
    record_type = struct.pack("B", 0)
    body = struct.pack("<iiii", root_id, header_id, 1, 0)
    return record_type + body


def _make_gzip_bf_header() -> bytes:
    """Return GZip-compressed minimal BinaryFormatter header bytes."""
    raw = _make_bf_header()
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
        gz.write(raw)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def minimal_bf_bytes() -> bytes:
    """Raw (uncompressed) minimal BinaryFormatter stream bytes."""
    return _make_bf_header()


@pytest.fixture()
def gzip_bf_bytes() -> bytes:
    """GZip-compressed minimal BinaryFormatter stream bytes."""
    return _make_gzip_bf_header()


@pytest.fixture()
def gzip_save_file(tmp_path: Path, gzip_bf_bytes: bytes) -> Path:
    """Write a minimal gzip BinaryFormatter file to a temp path."""
    save_path = tmp_path / "playerInfo.dat"
    save_path.write_bytes(gzip_bf_bytes)
    return save_path


@pytest.fixture()
def empty_save_data() -> SaveData:
    """A default empty SaveData instance."""
    return SaveData(source_file="test.dat")
