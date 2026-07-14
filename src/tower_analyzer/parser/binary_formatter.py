"""BinaryFormatterParser - decode a .NET BinaryFormatter byte stream.

Status: INCOMPLETE - full decoding requires mapping the Unity IL2CPP type
metadata embedded in the stream.

The .NET BinaryFormatter format (MS-NRBF) encodes objects with type
information, field names, and values.  Decoding Unity/IL2CPP-compiled saves
requires matching the serialized type names to the C# class definitions.

Reference:
    MS-NRBF: https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-nrbf

TODO:
    1. Parse the SerializationHeaderRecord (record type 0).
    2. Parse ClassWithMembersAndTypes records for SaveLoad.PlayerData.
    3. Recursively decode nested objects (Workshop, Labs, etc.).
    4. Map field names to Pydantic model attributes.
"""

from __future__ import annotations

import io
import logging
import struct
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# MS-NRBF record type identifiers (partial list)
# ---------------------------------------------------------------------------
RECORD_TYPE_SERIALIZATION_HEADER = 0
RECORD_TYPE_CLASS_WITH_ID = 1
RECORD_TYPE_SYSTEM_CLASS_WITH_MEMBERS = 2
RECORD_TYPE_CLASS_WITH_MEMBERS = 3
RECORD_TYPE_SYSTEM_CLASS_WITH_MEMBERS_AND_TYPES = 4
RECORD_TYPE_CLASS_WITH_MEMBERS_AND_TYPES = 5
RECORD_TYPE_BINARY_OBJECT_STRING = 6
RECORD_TYPE_BINARY_ARRAY = 7
RECORD_TYPE_MEMBER_PRIMITIVE_TYPED = 8
RECORD_TYPE_MEMBER_REFERENCE = 9
RECORD_TYPE_OBJECT_NULL = 10
RECORD_TYPE_MESSAGE_END = 11
RECORD_TYPE_BINARY_LIBRARY = 12
RECORD_TYPE_OBJECT_NULL_MULTIPLE_256 = 13
RECORD_TYPE_OBJECT_NULL_MULTIPLE = 14
RECORD_TYPE_ARRAY_SINGLE_PRIMITIVE = 15
RECORD_TYPE_ARRAY_SINGLE_OBJECT = 16
RECORD_TYPE_ARRAY_SINGLE_STRING = 17


class BinaryFormatterError(Exception):
    """Raised when BinaryFormatter decoding fails."""


@dataclass
class RawObject:
    """Raw representation of a deserialized .NET object.

    Stores the class name and a flat dict of field name → raw value.
    Higher layers are responsible for mapping this to typed Pydantic models.
    """

    class_name: str
    library_name: str
    fields: dict[str, Any] = field(default_factory=dict)
    object_id: int = 0


class BinaryFormatterParser:
    """Decode a .NET BinaryFormatter (MS-NRBF) byte stream.

    This is a best-effort partial decoder.  It reads the stream header and
    attempts to extract the root object and its fields.

    TODO:
        - Implement full recursive object graph decoding.
        - Handle all BinaryArray variants.
        - Decode primitive type arrays (int[], float[], etc.).
        - Map Unity IL2CPP type names to model classes.
    """

    def parse(self, data: bytes) -> RawObject:
        """Decode a BinaryFormatter stream and return the root object.

        Parameters
        ----------
        data:
            Raw decompressed bytes from GzipParser.

        Returns
        -------
        RawObject
            Root-level deserialized object with any fields that could be
            extracted.  Unknown fields are skipped with a warning.

        Raises
        ------
        BinaryFormatterError
            If the stream does not start with a valid serialization header.
        """
        reader = io.BytesIO(data)
        logger.debug("Parsing BinaryFormatter stream (%d bytes)", len(data))

        header = self._read_serialization_header(reader)
        logger.debug("Header: root_id=%d, header_id=%d", header["root_id"], header["header_id"])

        # TODO: implement full recursive decode of the object graph.
        # For now, return a placeholder object with the header metadata.
        root = RawObject(
            class_name="SaveLoad.PlayerData",
            library_name="Assembly-CSharp",
            fields={"_header": header},
            object_id=header["root_id"],
        )

        logger.warning(
            "BinaryFormatter decoding is incomplete. "
            "Only the stream header has been read. "
            "See TODO items in binary_formatter.py."
        )

        return root

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _read_serialization_header(self, reader: io.BytesIO) -> dict[str, int]:
        """Read and validate the MS-NRBF SerializationHeaderRecord.

        The record is always first in the stream and has a fixed structure:
            byte   record_type  (must be 0)
            int32  root_id
            int32  header_id
            int32  major_version (must be 1)
            int32  minor_version (must be 0)

        Raises
        ------
        BinaryFormatterError
            If the header is missing or malformed.
        """
        record_type_byte = reader.read(1)
        if not record_type_byte:
            raise BinaryFormatterError("Empty stream - no serialization header found")

        (record_type,) = struct.unpack("B", record_type_byte)
        if record_type != RECORD_TYPE_SERIALIZATION_HEADER:
            raise BinaryFormatterError(
                f"Expected SerializationHeaderRecord (type 0), got type {record_type}"
            )

        raw = reader.read(16)
        if len(raw) < 16:
            raise BinaryFormatterError("Stream too short to contain a valid header")

        root_id, header_id, major, minor = struct.unpack("<iiii", raw)

        if major != 1 or minor != 0:
            raise BinaryFormatterError(
                f"Unexpected BinaryFormatter version {major}.{minor} (expected 1.0)"
            )

        return {
            "root_id": root_id,
            "header_id": header_id,
            "major_version": major,
            "minor_version": minor,
        }

    @staticmethod
    def _read_string(reader: io.BytesIO) -> str:
        """Read a length-prefixed UTF-8 string (7-bit encoded length)."""
        length = 0
        shift = 0
        while True:
            b = reader.read(1)
            if not b:
                raise BinaryFormatterError("Unexpected end of stream reading string length")
            (byte_val,) = struct.unpack("B", b)
            length |= (byte_val & 0x7F) << shift
            if not (byte_val & 0x80):
                break
            shift += 7
        return reader.read(length).decode("utf-8", errors="replace")
