from __future__ import annotations

import gzip
import hashlib
from dataclasses import dataclass
from pathlib import Path

GZIP_MAGIC = b"\x1f\x8b"
DEFAULT_MAX_DECOMPRESSED_SIZE = 32 * 1024 * 1024


class SaveInspectionError(ValueError):
    """Raised when a save cannot be inspected safely."""


@dataclass(frozen=True, slots=True)
class SaveInspection:
    path: Path
    compressed_size: int
    decompressed_size: int
    sha256: str
    compression: str
    payload_type: str


def _detect_payload_type(payload: bytes) -> str:
    if len(payload) >= 17 and payload[0] == 0:
        return "probable-dotnet-nrbf"
    return "unknown-binary"


def _decompress_limited(path: Path, max_size: int) -> bytes:
    chunks: list[bytes] = []
    total = 0

    try:
        with gzip.open(path, "rb") as stream:
            while chunk := stream.read(64 * 1024):
                total += len(chunk)
                if total > max_size:
                    raise SaveInspectionError(
                        f"Decompressed payload exceeds safety limit of {max_size} bytes"
                    )
                chunks.append(chunk)
    except (OSError, EOFError) as exc:
        raise SaveInspectionError(f"Invalid or corrupted GZip payload: {exc}") from exc

    return b"".join(chunks)


def inspect_save(
    path: Path,
    *,
    max_decompressed_size: int = DEFAULT_MAX_DECOMPRESSED_SIZE,
) -> SaveInspection:
    """Inspect a save without deserializing or executing its payload."""
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise SaveInspectionError(f"Save file does not exist: {resolved}")

    compressed_size = resolved.stat().st_size
    with resolved.open("rb") as stream:
        magic = stream.read(2)

    if magic != GZIP_MAGIC:
        raise SaveInspectionError("Unsupported save format: expected a GZip header")

    digest = hashlib.sha256(resolved.read_bytes()).hexdigest()
    payload = _decompress_limited(resolved, max_decompressed_size)

    return SaveInspection(
        path=resolved,
        compressed_size=compressed_size,
        decompressed_size=len(payload),
        sha256=digest,
        compression="gzip",
        payload_type=_detect_payload_type(payload),
    )
