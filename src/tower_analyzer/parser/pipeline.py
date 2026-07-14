"""ParserPipeline - orchestrates the full parse pipeline.

Composes GzipParser → BinaryFormatterParser → ObjectGraph → SaveDataSerializer
into a single entry point.
"""

from __future__ import annotations

import logging
from pathlib import Path

from tower_analyzer.models.save_data import SaveData
from tower_analyzer.parser.binary_formatter import BinaryFormatterParser
from tower_analyzer.parser.gzip_parser import GzipParser
from tower_analyzer.parser.object_graph import ObjectGraph
from tower_analyzer.parser.serializer import SaveDataSerializer

logger = logging.getLogger(__name__)


class ParserPipeline:
    """End-to-end parse pipeline for playerInfo.dat files.

    This class composes all parser stages and returns a :class:`SaveData`.

    Usage::

        pipeline = ParserPipeline()
        save_data = pipeline.parse(Path("playerInfo.dat"))
    """

    def __init__(self) -> None:
        self._gzip = GzipParser()
        self._bf = BinaryFormatterParser()
        self._graph = ObjectGraph()
        self._serializer = SaveDataSerializer()

    def parse(self, path: Path) -> SaveData:
        """Parse a playerInfo.dat file end-to-end.

        Parameters
        ----------
        path:
            Path to the playerInfo.dat file.

        Returns
        -------
        SaveData
            Fully populated (or partially populated) save data model.

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        GzipParseError
            If GZip decompression fails.
        BinaryFormatterError
            If the .NET stream header is invalid.
        """
        logger.info("Starting parse pipeline for %s", path)

        # Stage 1 - decompress
        raw = self._gzip.decompress(path)
        raw_size = path.stat().st_size
        logger.debug("Stage 1 complete: %d compressed → %d decompressed bytes", raw_size, len(raw))

        # Stage 2 - decode BinaryFormatter
        root_obj = self._bf.parse(raw)
        logger.debug("Stage 2 complete: root class=%s", root_obj.class_name)

        # Stage 3 - resolve object graph
        resolved = self._graph.resolve([root_obj], root_id=root_obj.object_id)
        logger.debug("Stage 3 complete: resolved object id=%d", resolved.object_id)

        # Stage 4 - serialize to SaveData model
        save_data = self._serializer.serialize(resolved, path)
        save_data.raw_bytes_size = raw_size
        logger.info("Parse pipeline complete: %d warnings", len(save_data.parse_warnings))

        return save_data
