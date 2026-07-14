from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import BinaryIO


class RecordType(IntEnum):
    SERIALIZED_STREAM_HEADER = 0
    CLASS_WITH_ID = 1
    SYSTEM_CLASS_WITH_MEMBERS = 2
    CLASS_WITH_MEMBERS = 3
    SYSTEM_CLASS_WITH_MEMBERS_AND_TYPES = 4
    CLASS_WITH_MEMBERS_AND_TYPES = 5
    BINARY_OBJECT_STRING = 6
    BINARY_ARRAY = 7
    MEMBER_PRIMITIVE_TYPED = 8
    MEMBER_REFERENCE = 9
    OBJECT_NULL = 10
    MESSAGE_END = 11
    BINARY_LIBRARY = 12
    OBJECT_NULL_MULTIPLE_256 = 13
    OBJECT_NULL_MULTIPLE = 14
    ARRAY_SINGLE_PRIMITIVE = 15
    ARRAY_SINGLE_OBJECT = 16
    ARRAY_SINGLE_STRING = 17
    METHOD_CALL = 21
    METHOD_RETURN = 22


@dataclass(frozen=True, slots=True)
class StreamHeader:
    root_id: int
    header_id: int
    major_version: int
    minor_version: int


class NrbfParseError(ValueError):
    """Raised when an NRBF stream is invalid or unsupported."""


def read_stream_header(stream: BinaryIO) -> StreamHeader:
    """Read only the fixed NRBF stream header.

    Full record parsing is deliberately deferred. This function never constructs
    application objects and exists as the first testable NRBF boundary.
    """
    record_type = stream.read(1)
    if record_type != bytes([RecordType.SERIALIZED_STREAM_HEADER]):
        raise NrbfParseError("NRBF stream does not start with SerializedStreamHeader")

    raw = stream.read(16)
    if len(raw) != 16:
        raise NrbfParseError("Truncated SerializedStreamHeader")

    values = [int.from_bytes(raw[index : index + 4], "little", signed=True) for index in range(0, 16, 4)]
    header = StreamHeader(*values)
    if header.major_version != 1 or header.minor_version != 0:
        raise NrbfParseError(
            f"Unsupported NRBF version {header.major_version}.{header.minor_version}"
        )
    return header
