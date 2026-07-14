from __future__ import annotations

import gzip
from pathlib import Path

import pytest

from tower_analyzer.parser.save_inspector import SaveInspectionError, inspect_save


def test_inspects_gzip_payload(tmp_path: Path) -> None:
    save_path = tmp_path / "playerInfo.dat"
    payload = b"\x00" + b"safe-fixture" * 20

    with gzip.open(save_path, "wb") as stream:
        stream.write(payload)

    result = inspect_save(save_path)

    assert result.compression == "gzip"
    assert result.decompressed_size == len(payload)
    assert result.payload_type == "probable-dotnet-nrbf"
    assert len(result.sha256) == 64


def test_rejects_non_gzip_file(tmp_path: Path) -> None:
    save_path = tmp_path / "playerInfo.dat"
    save_path.write_bytes(b"not-gzip")

    with pytest.raises(SaveInspectionError, match="expected a GZip header"):
        inspect_save(save_path)


def test_enforces_decompressed_size_limit(tmp_path: Path) -> None:
    save_path = tmp_path / "playerInfo.dat"

    with gzip.open(save_path, "wb") as stream:
        stream.write(b"x" * 1024)

    with pytest.raises(SaveInspectionError, match="exceeds safety limit"):
        inspect_save(save_path, max_decompressed_size=128)
