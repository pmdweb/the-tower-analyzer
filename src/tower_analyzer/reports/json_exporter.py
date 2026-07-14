"""JSON exporter - export a SaveData to account.json."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from tower_analyzer.models.save_data import SaveData

logger = logging.getLogger(__name__)


class JsonExporter:
    """Export a :class:`SaveData` to a structured JSON file (account.json).

    Usage::

        exporter = JsonExporter()
        exporter.export(save_data, Path("account.json"))
    """

    def export(self, save: SaveData, output_path: Path) -> None:
        """Serialize *save* to JSON and write to *output_path*.

        The project MUST NOT modify save files.  This exporter writes
        only to the specified *output_path* and never touches the source.

        Parameters
        ----------
        save:
            Parsed save data to export.
        output_path:
            Destination path for the JSON file.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        data = save.model_dump(mode="json")
        json_text = json.dumps(data, indent=2, ensure_ascii=False, default=str)
        output_path.write_text(json_text, encoding="utf-8")
        logger.info("Exported save data to %s (%d bytes)", output_path, len(json_text))

    def to_json_str(self, save: SaveData, *, indent: int = 2) -> str:
        """Serialize *save* to a JSON string without writing to disk.

        Parameters
        ----------
        save:
            Parsed save data.
        indent:
            JSON indentation level.

        Returns
        -------
        str
            Pretty-printed JSON string.
        """
        data = save.model_dump(mode="json")
        return json.dumps(data, indent=indent, ensure_ascii=False, default=str)
