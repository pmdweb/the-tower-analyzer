"""GzipParser - decompress the outer GZip wrapper of playerInfo.dat."""

from __future__ import annotations

import gzip
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class GzipParseError(Exception):
    """Raised when GZip decompression fails."""


class GzipParser:
    """Decompresses a GZip-encoded file and returns raw bytes.

    playerInfo.dat is a GZip-compressed .NET BinaryFormatter stream.
    This parser handles only the decompression step.

    Usage::

        parser = GzipParser()
        raw_bytes = parser.decompress(Path("playerInfo.dat"))
    """

    def decompress(self, path: Path) -> bytes:
        """Decompress a GZip file and return raw inner bytes.

        Parameters
        ----------
        path:
            Path to the GZip-compressed file.

        Returns
        -------
        bytes
            Decompressed raw bytes ready for BinaryFormatter parsing.

        Raises
        ------
        GzipParseError
            If the file cannot be opened or is not valid GZip.
        FileNotFoundError
            If the path does not exist.
        """
        if not path.exists():
            raise FileNotFoundError(f"Save file not found: {path}")

        logger.debug("Decompressing %s (%d bytes)", path, path.stat().st_size)

        max_decompressed_bytes = 50 * 1024 * 1024  # 50 MiB safety limit
        try:
            with gzip.open(path, "rb") as fh:
                chunks: list[bytes] = []
                total = 0
                while True:
                    chunk = fh.read(1024 * 1024)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > max_decompressed_bytes:
                        raise GzipParseError(
                            f"Decompressed data exceeds {max_decompressed_bytes} bytes; aborting"
                        )
                    chunks.append(chunk)
                data = b"".join(chunks)
        except (OSError, gzip.BadGzipFile) as exc:
            raise GzipParseError(f"Failed to decompress {path}: {exc}") from exc

        logger.debug("Decompressed to %d bytes", len(data))
        return data

    def decompress_bytes(self, data: bytes) -> bytes:
        """Decompress raw GZip bytes and return the inner payload.

        Parameters
        ----------
        data:
            GZip-compressed bytes.

        Returns
        -------
        bytes
            Decompressed payload.

        Raises
        ------
        GzipParseError
            If the input is not valid GZip data.
        """
        try:
            return gzip.decompress(data)
        except (OSError, gzip.BadGzipFile) as exc:
            raise GzipParseError(f"Failed to decompress bytes: {exc}") from exc
