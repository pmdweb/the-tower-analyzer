#!/usr/bin/env python3
"""generate_sample_save.py – create a minimal synthetic playerInfo.dat for testing.

This script generates a GZip-wrapped BinaryFormatter header file that can be
used for smoke testing the parser pipeline without a real save file.

Usage:
    python scripts/generate_sample_save.py [output_path]

The generated file is NOT a real save – it contains only the minimum bytes
needed to exercise the GzipParser and BinaryFormatterParser header reading.
"""

from __future__ import annotations

import gzip
import io
import struct
import sys
from pathlib import Path


def make_minimal_bf_stream() -> bytes:
    """Build a minimal MS-NRBF serialization header stream."""
    # SerializationHeaderRecord: record_type=0, root_id=1, header_id=-1, major=1, minor=0
    record_type = struct.pack("B", 0)
    body = struct.pack("<iiii", 1, -1, 1, 0)
    # MessageEnd record (record_type=11)
    end = struct.pack("B", 11)
    return record_type + body + end


def main() -> None:
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("examples/sample_save/playerInfo.dat")
    output.parent.mkdir(parents=True, exist_ok=True)

    raw = make_minimal_bf_stream()

    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
        gz.write(raw)

    output.write_bytes(buf.getvalue())
    print(f"Generated {output} ({output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
