"""ObjectGraph - reconstruct the Unity IL2CPP object graph from raw objects.

Takes the flat list of RawObjects produced by BinaryFormatterParser and
resolves object references into a hierarchical structure.

Status: INCOMPLETE - pending full BinaryFormatter decode.

TODO:
    1. Receive all RawObject records from the BinaryFormatter stream.
    2. Build an id → RawObject registry.
    3. Resolve MemberReference records to their referenced objects.
    4. Recursively populate nested objects (Workshop, Labs, etc.) under
       the root SaveLoad.PlayerData object.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from tower_analyzer.parser.binary_formatter import RawObject

logger = logging.getLogger(__name__)


class ObjectGraphError(Exception):
    """Raised when the object graph cannot be resolved."""


@dataclass
class ResolvedObject:
    """An object whose references have been resolved.

    After resolution, ``fields`` contains either primitive values or other
    ``ResolvedObject`` instances (no dangling integer references remain).
    """

    class_name: str
    library_name: str
    fields: dict[str, Any] = field(default_factory=dict)
    object_id: int = 0


class ObjectGraph:
    """Resolve a flat list of RawObjects into a rooted object graph.

    Usage::

        graph = ObjectGraph()
        root = graph.resolve([raw_obj1, raw_obj2, ...], root_id=1)
    """

    def resolve(self, raw_objects: list[RawObject], root_id: int) -> ResolvedObject:
        """Resolve a flat list of raw objects into a rooted graph.

        Parameters
        ----------
        raw_objects:
            All deserialized RawObjects from BinaryFormatterParser.
        root_id:
            The object_id of the root object (SaveLoad.PlayerData).

        Returns
        -------
        ResolvedObject
            Resolved root object.

        Raises
        ------
        ObjectGraphError
            If the root_id is not found in the provided objects.
        """
        # TODO: implement full reference resolution.
        # For now, wrap the first RawObject as the resolved root.
        registry: dict[int, RawObject] = {obj.object_id: obj for obj in raw_objects}

        if root_id not in registry:
            if not raw_objects:
                raise ObjectGraphError("No raw objects provided to resolve")
            # Fallback: use the first object
            root_raw = raw_objects[0]
            logger.warning(
                "Root object id=%d not found; falling back to first object id=%d",
                root_id,
                root_raw.object_id,
            )
        else:
            root_raw = registry[root_id]

        logger.warning(
            "ObjectGraph resolution is incomplete. "
            "Full reference resolution requires a complete BinaryFormatter decode."
        )

        return ResolvedObject(
            class_name=root_raw.class_name,
            library_name=root_raw.library_name,
            fields=dict(root_raw.fields),
            object_id=root_raw.object_id,
        )
